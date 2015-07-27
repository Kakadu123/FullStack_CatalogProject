from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Categories, Base, Items

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


# First Category
animalCat1 = Categories(name="amphibians", id="1")

session.add(animalCat1)
session.commit()


species1 = Items(name="Newts", description="Newts and salamanders ", categories=animalCat1)

session.add(species1)
session.commit()

species2 = Items(name="Frogs", description="Frogs are a diverse and largely carnivorous group of short-bodied, tailless amphibians composing the order Anura (Ancient Greek an-, without + oura, tail). The oldest fossil 'proto-frog' appeared in the early Triassic of Madagascar, but molecular clock dating suggests their origins may extend further back to the Permian, 265 million years ago. Frogs are widely distributed, ranging from the tropics to subarctic regions, but the greatest concentration of species diversity is found in tropical rainforests. There are approximately 4,800 recorded species, accounting for over 85 percent extant amphibian species. They are also one of the five most diverse vertebrate orders.", categories=animalCat1)

session.add(species2)
session.commit()

# Second Category
animalCat2 = Categories(name="reptiles", id="2")

session.add(animalCat2)
session.commit()


species1 = Items(name="Snakes", description="bad creatiors", categories=animalCat2)

session.add(species1)
session.commit()

species2 = Items(name="Lizards", description="Frogs like ", categories=animalCat2)

session.add(species2)
session.commit()


print "added items!"
