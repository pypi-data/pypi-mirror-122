
# Class: geographic exposure


A geographic exposure is a factor relating to geographic proximity to some impactful entity.

URI: [biolink:GeographicExposure](https://w3id.org/biolink/vocab/GeographicExposure)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing],[GeographicLocation],[GeographicExposure&#124;timepoint:time_type%20%3F;latitude(i):float%20%3F;longitude(i):float%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[ExposureEvent],[GeographicLocation]^-[GeographicExposure],[ExposureEvent],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing],[GeographicLocation],[GeographicExposure&#124;timepoint:time_type%20%3F;latitude(i):float%20%3F;longitude(i):float%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[ExposureEvent],[GeographicLocation]^-[GeographicExposure],[ExposureEvent],[Attribute],[Agent])

## Parents

 *  is_a: [GeographicLocation](GeographicLocation.md) - a location that can be described in lat/long coordinates

## Uses Mixin

 *  mixin: [ExposureEvent](ExposureEvent.md) - A (possibly time bounded) incidence of a feature of the environment of an organism that influences one or more phenotypic features of that organism, potentially mediated by genes

## Attributes


### Inherited from geographic location:

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
 * [latitude](latitude.md)  <sub>0..1</sub>
     * Description: latitude
     * Range: [Float](types/Float.md)
 * [longitude](longitude.md)  <sub>0..1</sub>
     * Description: longitude
     * Range: [Float](types/Float.md)

### Mixed in from exposure event:

 * [timepoint](timepoint.md)  <sub>0..1</sub>
     * Description: a point in time
     * Range: [TimeType](types/TimeType.md)
