from unittest import TestCase


from fluxture.db import (
    AutoIncrement, column_options, ColumnOptions, Database, default, ForeignKey, Model, primary_key, Table
)


class Person(Model):
    name: primary_key(str)
    age: int


class TestDatabase(TestCase):
    def test_create_table(self):
        db = Database()
        table = db.create_table("people", Table[Person])
        self.assertEqual(len(table), 0)
        person = Person(name="Foo", age=1337)
        table.append(person)
        self.assertEqual(len(table), 1)
        retrieved_person = next(iter(table))
        self.assertIsInstance(retrieved_person, Person)
        self.assertEqual(retrieved_person, person)
        self.assertEqual(next(iter(table.select(age=1337))), person)
        self.assertCountEqual(table.select(age=0), ())

    def test_define_db(self):
        class TestDB(Database):
            people: Table[Person]

        db = TestDB()
        self.assertEqual(len(db.people), 0)

    def test_primary_key(self):
        self.assertEqual(Person.primary_key_name, "name")

        class NoPrimaryKey(Model):
            not_primary_key: int
            not_primary_key_either: float

        self.assertEqual(NoPrimaryKey.primary_key_name, "rowid")

    def test_default(self):
        class Number(Model):
            n: default(primary_key(int), 1)

        class TestDB(Database):
            numbers: Table[Number]

        db = TestDB()
        db.numbers.append(Number())
        self.assertEqual(next(iter(db.numbers)), Number(1))

    def test_foreign_key(self):
        class Height(Model):
            person: primary_key(ForeignKey["people", Person])  # noqa: F821
            height: int

        class TestDB(Database):
            people: Table[Person]
            heights: Table[Height]

        db = TestDB()
        person = Person(name="Foo", age=1337)
        db.people.append(person)
        db.heights.append(Height(person="Foo", height=80))
        h = next(iter(db.heights))
        self.assertEqual(h.person, person)

    def test_auto_increment(self):
        class Counter(Model):
            id: column_options(AutoIncrement, ColumnOptions(primary_key=True, auto_increment=True))

        class TestDB(Database):
            counters: Table[Counter]

        db = TestDB()
        counter = Counter()
        self.assertIsInstance(counter.id, AutoIncrement)
        self.assertEqual(counter.id.initialized, False)
        self.assertTrue(any(key == "id" for key, _ in counter.uninitialized_auto_increments()))
        db.counters.append(counter)
        self.assertEqual(counter.id.initialized, True)
