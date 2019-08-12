import pynini

chars = ([chr(i) for i in range(1, 91)] + ["\\[", "\\]", "\\\\"] + [chr(i) for i in range(94, 256)])
sigma_star = pynini.union(*chars).closure()
sigma_star.optimize()


input_string = "Do you have Camembert or Edam?"     # Do you have <cheese>Camembert</cheese> or <cheese>Edam</cheese>?
cheeses = ("Boursin", "Camembert", "Cheddar", "Edam", "Gruyere", "Ilchester", "Jarlsberg", "Red Leicester", "Stilton")
output_string = "Do you have <cheese>Camembert</cheese> or <cheese>Edam</cheese>"

fst_target = pynini.string_map(cheeses)
ltag = pynini.transducer("", "<cheese>")
rtag = pynini.transducer("", "</cheese>")
substitution = ltag + fst_target + rtag

rewrite = pynini.cdrewrite(substitution, "", "", sigma_star)
output = pynini.compose(input_string, rewrite).stringify()


#######################################################################################################################

singular_map = pynini.union(
    pynini.transducer("feet", "foot"),
    pynini.transducer("pence", "penny"),

    # Any sequence of bytes ending in "ches" strips the "es";
    # the last argument -1 is a "weight" that gives this analysis a higher priority, if it matches the input.
    sigma_star + pynini.transducer("ches", "ch", -1),

    # Any sequence of bytes ending in "s" strips the "s".
    sigma_star + pynini.transducer("s", "")
)

rc = pynini.union(".", ",", "!", ";", "?", " ", "[EOS]")
singularize = pynini.cdrewrite(singular_map, " 1 ", rc, sigma_star)
singularize.optimize(compute_props=True)

# singularize = pynini.epsnormalize(singularize, eps_norm_output=True)
# singularize = pynini.disambiguate(singularize)
# determ_singularize = pynini.determinize(singularize, det_type="nonfunctional")
# determ_singularize.minimize(allow_nondet=False)

singularize.draw('/home/m.domrachev/repos/attribute_parser/grammar_fst/Pynini/singularize.dot')
singularize.write('/home/m.domrachev/repos/attribute_parser/grammar_fst/Pynini/singularize.fst')


def _singularize(string):
    return pynini.shortestpath(
        pynini.compose(string.strip(), singularize)).stringify()


print(_singularize("The current temperature in New York is 1 degrees"))

