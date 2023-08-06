# Stems
A stem is what [inflectional morphological processes](../inflections) are applied to to form a valid [wordform](../wordforms).
Inflectional morphology may not be needed for a valid form.
Stems can be [morphologically complex](../stemparts), being formed by processes like [derivation](../derivations) or composition (not yet modeled).

## StemTable: `stems.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | singlevalued | A reference to a language (or variety) the stem belongs to<br>References LanguageTable
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | singlevalued | <div> <p>A title, name or label for an entity.</p> </div> 
`Lexeme_ID` | `string` | singlevalued | The lexeme this stem belongs to.<br>References lexemes.csv.
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | unspecified | A reference to the meaning denoted by the stem<br>References ParameterTable
`Morpho_Segments` | list of `string` (separated by ` `) | multivalued | A representation of the morphologically segmented stem.
`Gloss_ID` | list of `string` (separated by `,`) | multivalued | The gloss the morph has in the wordform.<br>References glosses.csv.
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | singlevalued | <div> <p> A human-readable comment on a resource, providing additional context. </p> </div> 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `; `) | multivalued | <div> <p>List of source specifications, of the form &lt;source_ID&gt;[], e.g. http://glottolog.org/resource/reference/id/318814[34], or meier2015[3-12] where meier2015 is a citation key in the accompanying BibTeX file.</p> </div> 