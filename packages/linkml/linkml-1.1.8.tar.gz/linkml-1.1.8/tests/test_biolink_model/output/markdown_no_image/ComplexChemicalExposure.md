
# Class: complex chemical exposure


A complex chemical exposure is an intake of a chemical mixture (e.g. gasoline), other than a drug.

URI: [biolink:ComplexChemicalExposure](https://w3id.org/biolink/vocab/ComplexChemicalExposure)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon],[NamedThing],[Mixture],[ComplexChemicalExposure&#124;timepoint(i):time_type%20%3F;is_metabolite(i):boolean%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[Mixture],[ChemicalExposure]^-[ComplexChemicalExposure],[ChemicalSubstance],[ChemicalExposure],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon],[NamedThing],[Mixture],[ComplexChemicalExposure&#124;timepoint(i):time_type%20%3F;is_metabolite(i):boolean%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[Mixture],[ChemicalExposure]^-[ComplexChemicalExposure],[ChemicalSubstance],[ChemicalExposure],[Attribute],[Agent])

## Parents

 *  is_a: [ChemicalExposure](ChemicalExposure.md) - A chemical exposure is an intake of a particular chemical substance, other than a drug.

## Uses Mixin

 *  mixin: [Mixture](Mixture.md) - The physical combination of two or more molecular entities in which the identities are retained and are mixed in the form of solutions, suspensions and colloids.

## Attributes


### Inherited from chemical exposure:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [type](type.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [name](name.md)  <sub>0..1</sub>
     * Description: A human-readable name for an attribute or entity.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a human-readable description of an entity
     * Range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [source](source.md)  <sub>0..1</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [provided by](provided_by.md)  <sub>0..\*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * Range: [Agent](Agent.md)
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Range: [NamedThing](NamedThing.md)
 * [is metabolite](is_metabolite.md)  <sub>0..1</sub>
     * Description: indicates whether a chemical substance is a metabolite
     * Range: [Boolean](types/Boolean.md)

### Mixed in from mixture:

 * [has constituent](has_constituent.md)  <sub>0..\*</sub>
     * Description: one or more chemical substances within a mixture
     * Range: [ChemicalSubstance](ChemicalSubstance.md)
