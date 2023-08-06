
# Class: procedure


A series of actions conducted in a certain order or manner

URI: [biolink:Procedure](https://w3id.org/biolink/vocab/Procedure)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Treatment]-%20has%20procedure%200..*>[Procedure&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Procedure]uses%20-.->[ActivityAndBehavior],[NamedThing]^-[Procedure],[Treatment],[NamedThing],[Attribute],[Agent],[ActivityAndBehavior])](https://yuml.me/diagram/nofunky;dir:TB/class/[Treatment]-%20has%20procedure%200..*>[Procedure&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Procedure]uses%20-.->[ActivityAndBehavior],[NamedThing]^-[Procedure],[Treatment],[NamedThing],[Attribute],[Agent],[ActivityAndBehavior])

## Parents

 *  is_a: [NamedThing](NamedThing.md) - a databased entity or concept/class

## Uses Mixin

 *  mixin: [ActivityAndBehavior](ActivityAndBehavior.md) - Activity or behavior of any independent integral living, organization or mechanical actor in the world

## Referenced by Class

 *  **[NamedThing](NamedThing.md)** *[has procedure](has_procedure.md)*  <sub>0..\*</sub>  **[Procedure](Procedure.md)**

## Attributes


### Inherited from named thing:

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

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | UMLSSG:PROC |
| **Narrow Mappings:** | | UMLSSC:T059 |
|  | | UMLSST:lbpr |
|  | | UMLSSC:T060 |
|  | | UMLSST:diap |
|  | | UMLSSC:T061 |
|  | | UMLSST:topp |
|  | | UMLSSC:T063 |
|  | | UMLSST:mbrt |

