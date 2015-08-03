from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Categories, Base, Items
import json

engine = create_engine('sqlite:///categoriesDB.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Entries to Categories and Items table
# Foreign key relation established

# Source Data for database import
data = [
    {
      "items": [
        {
          "description": "A newt is a semiaquatic amphibian of the family Salamandridae, although not all aquatic salamanders are considered newts. Newts are classified as a part of the salamandrid subfamily Pleurodelinae, and can be found in North America, Europe and Asia. Newts metamorphose through three distinct developmental life stages: aquatic larva, terrestrial juvenile (called an eft[2]), and adult. Adult newts have lizard-like bodies and may be either fully aquatic, living permanently in the water, or semiaquatic, living terrestrially, but returning to the water every year to breed. (Source: Wikipedia)",
          "category_id": 1,
          "name": "Newts",
          "id": 1
        },
        {
          "description": "Frogs are a diverse and largely carnivorous group of short-bodied, tailless amphibians composing the order Anura (Ancient Greek an-, without + oura, tail). The oldest fossil 'proto-frog' appeared in the early Triassic of Madagascar, but molecular clock dating suggests their origins may extend further back to the Permian, 265 million years ago. Frogs are widely distributed, ranging from the tropics to subarctic regions, but the greatest concentration of species diversity is found in tropical rainforests. There are approximately 4,800 recorded species, accounting for over 85 percent extant amphibian species. They are also one of the five most diverse vertebrate orders. (Source: Wikipedia)",
          "category_id": 1,
          "name": "Frogs",
          "id": 2
        },
        {
          "description": "The caecilians (New Latin, blind ones) are an order (Gymnophiona) of limbless, serpentine amphibians. They mostly live hidden in the ground, making them the least familiar order of amphibians. All extant caecilians and their closest fossil relatives are grouped as the clade Apoda. They are mostly distributed in the tropics of South and Central America, Africa, and southern Asia. The diets of caecilians are not well known. (Source: Wikipedia)",
          "category_id": 1,
          "name": "Caecilians",
          "id": 3
        }
      ],
      "category_id": 1,
      "category_name": "Amphibians"
    },
    {
      "items": [
        {
          "description": "Snakes are elongated, legless, carnivorous reptiles of the suborder Serpentes that can be distinguished from legless lizards by their lack of eyelids and external ears. Like all squamates, snakes are ectothermic, amniote vertebrates covered in overlapping scales. Many species of snakes have skulls with several more joints than their lizard ancestors, enabling them to swallow prey much larger than their heads with their highly mobile jaws. To accommodate their narrow bodies, snakes' paired organs (such as kidneys) appear one in front of the other instead of side by side, and most have only one functional lung. Some species retain a pelvic girdle with a pair of vestigial claws on either side of the cloaca. (Source: Wikipedia)",
          "category_id": 2,
          "name": "Snakes",
          "id": 4
        },
        {
          "description": "The Crocodilia (or Crocodylia) are an order of large, predatory, semiaquatic reptiles. They appeared 83.5 million years ago in the Late Cretaceous period (Campanian stage) and are the closest living relatives of birds, as the two groups are the only known survivors of the Archosauria. Members of the crocodilian total group, the clade Pseudosuchia, appeared about 250 million years ago in the Early Triassic period, and diversified during the Mesozoic era. The order Crocodilia includes the true crocodiles (family Crocodylidae), the alligators and caimans (family Alligatoridae), and the gharial and false gharial (family Gavialidae). Although the term 'crocodiles' is sometimes used to refer to all of these, a less ambiguous vernacular term for this group is crocodilians. (Source: Wikipedia)",
          "category_id": 2,
          "name": "Crocodilians",
          "id": 5
        },
        {
          "description": "The Squamata, or the scaled reptiles, are the largest recent order of reptiles, comprising all lizards and snakes. With over 9,000 species, it is also the second-largest order of vertebrates, after the perciform fish. Members of the order are distinguished by their skins, which bear horny scales or shields. They also possess movable quadrate bones, making it possible to move the upper jaw relative to the neurocranium. This is particularly visible in snakes, which are able to open their mouths very wide to accommodate comparatively large prey. They are the most variably sized order of reptiles, ranging from the 16 mm (0.63 in) dwarf gecko (Sphaerodactylus ariasae) to the 5.21 m (17.1 ft) green anaconda (Eunectes murinus) and the now-extinct mosasaurs, which reached lengths of 14 m (46 ft). (Source: Wikipedia)",
          "category_id": 2,
          "name": "Squamata",
          "id": 6
        },
        {
          "description": "Turtles are reptiles of the order Testudines (or Chelonii) characterised by a special bony or cartilaginous shell developed from their ribs and acting as a shield. 'Turtle' may refer to the order as a whole (American English) or to fresh-water and sea-dwelling testudines (British English). The order Testudines includes both extant (living) and extinct species. The earliest known members of this group date from 157 million years ago, making turtles one of the oldest reptile groups and a more ancient group than snakes or crocodilians. Of the 327 known species alive today, some are highly endangered. Turtles are ectotherms their internal temperature varies according to the ambient environment, commonly called cold-blooded. However, because of their high metabolic rate, leatherback sea turtles have a body temperature that is noticeably higher than that of the surrounding water. (Source: Wikipedia)",
          "category_id": 2,
          "name": "Turtles",
          "id": 7
        }
      ],
      "category_id": 2,
      "category_name": "Reptiles"
    },
    {
      "items": [
        {
          "description": "Birds of prey, also known as raptors, hunt and feed on other animals. The term 'raptor' is derived from the Latin word rapere (meaning to seize or take by force).[1] These birds are characterized by keen vision that allows them to detect prey during flight and powerful talons and beaks. Many species of birds may be considered partly or exclusively predatory. However, in ornithology, the term 'bird of prey' applies only to birds of the families listed below. Taken literally, the term 'bird of prey' has a wide meaning that includes many birds that hunt and feed on animals and also birds that eat very small insects. In ornithology, the definition for 'bird of prey' has a narrower meaning: birds that have very good eyesight for finding food, strong feet for holding food, and a strong curved beak for tearing flesh. Most birds of prey also have strong curved talons for catching or killing prey. (Source: Wikipedia)",
          "category_id": 3,
          "name": "Birds of Prey",
          "id": 8
        },
        {
          "description": "Cranes are a clade (Gruidae) of large, long-legged and long-necked birds in the group Gruiformes. There are fifteen species of crane in four genera. Unlike the similar-looking but unrelated herons, cranes fly with necks outstretched, not pulled back. Cranes live on all continents except Antarctica and South America. Most species of cranes are at the least classified as threatened, if not critically endangered, within their range. The plight of the whooping cranes of North America inspired some of the first US legislation to protect endangered species. (Source: Wikipedia)",
          "category_id": 3,
          "name": "Cranes",
          "id": 9
        },
        {
          "description": "Kingfishers are a group of small to medium-sized brightly colored birds in the order Coraciiformes. They have a cosmopolitan distribution, with most species found outside of the Americas. The group is treated either as a single family, Alcedinidae, or as a suborder Alcedines containing three families, Alcedinidae (river kingfishers), Halcyonidae (tree kingfishers), and Cerylidae (water kingfishers). There are roughly 90 species of kingfisher. All have large heads, long, sharp, pointed bills, short legs, and stubby tails. Most species have bright plumage with little differences between the sexes. Most species are tropical in distribution, and a slight majority are found only in forests. (Source: Wikipedia)",
          "category_id": 3,
          "name": "Kingfishers",
          "id": 10
        }
      ],
      "category_id": 3,
      "category_name": "Birds"
    },
    {
      "items": [
        {
          "description": "The aardvark is a medium-sized, burrowing, nocturnal mammal native to Africa.[2] It is the only living species of the order Tubulidentata,[3][4] although other prehistoric species and genera of Tubulidentata are known. Unlike other insectivores, it has a long pig-like snout, which is used to sniff out food. It roams over most of the southern two-thirds of the African continent, avoiding mainly rocky areas. A nocturnal feeder, it subsists on ants and termites, which it will dig out of their hills using its sharp claws and powerful legs. It also digs to create burrows in which to live and rear its young. It receives a 'least concern' rating from the IUCN, although its numbers seem to be decreasing. (Source: Wikipedia)",
          "category_id": 4,
          "name": "Aardvark",
          "id": 11
        },
        {
          "description": "Bats are mammals of the order Chiroptera whose forelimbs form webbed wings, making them the only mammals naturally capable of true and sustained flight. By contrast, other mammals said to fly, such as flying squirrels, gliding possums, and colugos, can only glide for short distances. Bats do not flap their entire forelimbs, as birds do, but instead flap their spread-out digits, which are very long and covered with a thin membrane or patagium. Bats are the second largest order of mammals (after the rodents), representing about 20 percent of all classified mammal species worldwide, with about 1,240 bat species divided into two suborders: the less specialized and largely fruit-eating megabats, or flying foxes, and the highly specialized and echolocating microbats. About 70 percent of bat species are insectivores. Most of the rest are frugivores, or fruit eaters. A few species, such as the fish-eating bat, feed from animals other than insects, with the vampire bats being hematophagous, or feeding on blood. (Source: Wikipedia)",
          "category_id": 4,
          "name": "Bats",
          "id": 12
        },
        {
          "description": "A carnivore meaning 'meat eater' (Latin, caro meaning 'meat' or 'flesh' and vorare meaning 'to devour') is an organism that derives its energy and nutrient requirements from a diet consisting mainly or exclusively of animal tissue, whether through predation or scavenging. Animals that depend solely on animal flesh for their nutrient requirements are called obligate carnivores while those that also consume non-animal food are called facultative carnivores. Omnivores also consume both animal and non-animal food, and apart from the more general definition, there is no clearly defined ratio of plant to animal material that would distinguish a facultative carnivore from an omnivore. A carnivore that sits at the top of the foodchain is termed an apex predator. (Source: Wikipedia)",
          "category_id": 4,
          "name": "Carnivores",
          "id": 13
        },
        {
          "description": "The infraorder Cetacea includes the marine mammals commonly known as whales, dolphins, and porpoises. Cetus is Latin and is used in biological names to mean 'whale'. Its original meaning, 'large sea animal', was more general. It comes from Ancient Greek, used for whales and huge fish or sea monsters. Cetology is the branch of marine science associated with the study of cetaceans. An ancient ancestor of the whale, Basilosaurus was thought to be a reptile until vestigial parts were recognized. Traditionally Cetacea was treated as an order, but it has become increasingly known based on physiological data that cetaceans are not only a clade of even-toed ungulates, but that Cetacea might be recognized as an infraorder. (Source: Wikipedia)",
          "category_id": 4,
          "name": "Cetaceans",
          "id": 14
        }
      ],
      "category_id": 4,
      "category_name": "Mammals"
    },
    {
      "items": [
        {
          "description": "Osteichthyes, also called bony fish, are a taxonomic group of fish that have bone, as opposed to cartilaginous, skeletons. The vast majority of fish are osteichthyes, which is an extremely diverse and abundant group consisting of 45 orders, and over 435 families and 28,000 species. It is the largest class of vertebrates in existence today. Osteichthyes are divided into the ray-finned fish (Actinopterygii) and lobe-finned fish (Sarcopterygii). The oldest known fossils of bony fish are about 420 million years ago, which are also transitional fossils, showing a tooth pattern that is in between the tooth rows of sharks and bony fishes. (Source: Wikipedia)",
          "category_id": 5,
          "name": "Bony Fishes",
          "id": 15
        },
        {
          "description": "Chondrichthyes or cartilaginous fishes are jawed vertebrates with paired fins, paired nares, scales, a heart with its chambers in series, and skeletons made of cartilage rather than bone. The class is divided into two subclasses: Elasmobranchii (sharks, rays, skates, and sawfish) and Holocephali (chimaeras, sometimes called ghost sharks, which are sometimes separated into their own class). Within the infraphylum Gnathostomata, cartilaginous fishes are distinct from all other jawed vertebrates, the extant members of which all fall into Teleostomi. (Source: Wikipedia)",
          "category_id": 5,
          "name": "Cartilaginous Fish",
          "id": 16
        },
        {
          "description": "Lampreys (sometimes also called lamprey eels) are any jawless fish of the order Petromyzontiformes. The adult lamprey may be characterized by a toothed, funnel-like sucking mouth. The common name 'lamprey' is probably derived from Latin lampetra, which may mean 'stone licker', though the etymology is uncertain. Currently there are about 38 known extant species of lampreys. Although they are well known for boring into the flesh of other fish to suck their blood, in fact only a minority do so;[5] only 18 species of lampreys are actually parasitic.[6] The lampreys are a very ancient lineage of vertebrates, though their exact relationship to hagfishes and jawed vertebrates is still a matter of dispute. (Source: Wikipedia)",
          "category_id": 5,
          "name": "Lampreys",
          "id": 17
        }
      ],
      "category_id": 5,
      "category_name": "Fish"
    },
    {
      "items": [
        {
          "description": "An arthropod is an invertebrate animal having an exoskeleton (external skeleton), a segmented body, and jointed appendages. Arthropods form the phylum Arthropoda, and include the insects, arachnids, myriapods, and crustaceans. Arthropods are characterized by their jointed limbs and cuticle made of chitin, often mineralised with calcium carbonate. The arthropod body plan consists of segments, each with a pair of appendages. The rigid cuticle inhibits growth, so arthropods replace it periodically by moulting. Their versatility has enabled them to become the most species-rich members of all ecological guilds in most environments. (Source: Wikipedia)",
          "category_id": 6,
          "name": "Arthropods",
          "id": 18
        },
        {
          "description": "Cnidaria is a phylum containing over 10,000[5] species of animals found exclusively in aquatic and mostly marine environments. Their distinguishing feature is cnidocytes, specialized cells that they use mainly for capturing prey. Their bodies consist of mesoglea, a non-living jelly-like substance, sandwiched between two layers of epithelium that are mostly one cell thick. They have two basic body forms: swimming medusae and sessile polyps, both of which are radially symmetrical with mouths surrounded by tentacles that bear cnidocytes. Both forms have a single orifice and body cavity that are used for digestion and respiration. (Source: Wikipedia)",
          "category_id": 6,
          "name": "Cnidarians",
          "id": 19
        },
        {
          "description": "Echinoderm is the common name given to any member of the Phylum Echinodermata of marine animals. The adults are recognizable by their (usually five-point) radial symmetry, and include such well-known animals as starfish, sea urchins, sand dollars, and sea cucumbers, as well as the sea lilies or 'stone lilies'. Echinoderms are found at every ocean depth, from the intertidal zone to the abyssal zone. The phylum contains about 7000 living species,[4] making it the second-largest grouping of deuterostomes (a superphylum), after the chordates (which include the vertebrates, such as birds, fishes, mammals, and reptiles). Echinoderms are also the largest phylum that has no freshwater or terrestrial (land-based) representatives. (Source: Wikipedia)",
          "category_id": 6,
          "name": "Echinoderms",
          "id": 20
        },
        {
          "description": "The molluscs or mollusks compose the large phylum of invertebrate animals known as the Mollusca. Around 85,000 extant species of molluscs are recognized. Molluscs are the largest marine phylum, comprising about 23 percent of all the named marine organisms. Numerous molluscs also live in freshwater and terrestrial habitats. They are highly diverse, not just in size and in anatomical structure, but also in behaviour and in habitat. The phylum is typically divided into 9 or 10 taxonomic classes, of which two are entirely extinct. Cephalopod molluscs, such as squid, cuttlefish and octopus, are among the most neurologically advanced of all invertebrates and either the giant squid or the colossal squid is the largest known invertebrate species. The gastropods (snails and slugs) are by far the most numerous molluscs in terms of classified species, and account for 80 percent of the total. The scientific study of molluscs is called malacology. (Source: Wikipedia)",
          "category_id": 6,
          "name": "Molluscs",
          "id": 21
        }
      ],
      "category_id": 6,
      "category_name": "Invertebrates"
    }
  ]

# Looping structure to import data
for x in range(0, len(data)):
    print "  ==  "
    print data[x]['category_name']

    cat = Categories(name=data[x]['category_name'], id=data[x]['category_id'])
    session.add(cat)
    session.commit()

    for y in range(0, len(data[x]['items'])):
        print(data[x]['items'][y]['name'])

        species = Items(name=data[x]['items'][y]['name'], description=data[x]['items'][y]['description'], categories=cat)
        session.add(species)
        session.commit()

print "added items!"
