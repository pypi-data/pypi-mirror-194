# Wordforms
Wordforms are units analyzed as grammatical words in a given language.
Although there has been some discussion as to the universality of such a concept, it is useful for the description of many languages.
The morphological segmentation of wordforms is stored in the `Parts` column via [an association table](../wordformparts).
`Stem_ID` optionally references a [stem](../stems) of which a wordform is an inflected form; wordforms are also connected to stems via [wordformstems](../formstems).

## WordformTable: `wordforms.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | singlevalued | A reference to a language (or variety) the form belongs to<br>References LanguageTable
[Form](http://cldf.clld.org/v1.0/terms.rdf#form) | `string` | singlevalued | The written expression of the form.
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | singlevalued | A human-readable description
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | unspecified | A reference to the meaning denoted by the form<br>References ParameterTable
[Morpho_Segments](http://cldf.clld.org/v1.0/terms.rdf#segments) | list of `string` (separated by ` `) | multivalued | A representation of the morphologically segmented form.
`Stem_ID` | `string` | singlevalued | The stem of which this wordform is an inflected form.<br>References stems.csv.
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | unspecified | <div> <p> A human-readable comment on a resource, providing additional context. </p> </div> 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | multivalued | <div> <p>List of source specifications, of the form &lt;source_ID&gt;[], e.g. http://glottolog.org/resource/reference/id/318814[34], or meier2015[3-12] where meier2015 is a citation key in the accompanying BibTeX file.</p> </div> 