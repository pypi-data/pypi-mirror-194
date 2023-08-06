


class RevolvingDoor:
    """
    The revolving door between politics and business is a phenomenon in economics characterized by the movement of individuals between high-level positions in government and the private sector. This movement can take various forms, including politicians taking jobs in the private sector after leaving office, private sector executives taking government positions, and individuals transitioning back and forth between the two sectors multiple times throughout their careers.

    This revolving door can create a number of potential conflicts of interest, as individuals may be influenced by their previous affiliations or future job prospects when making decisions in their current roles. Additionally, the revolving door can contribute to the concentration of power among a small group of elite individuals who move between government and business, potentially limiting opportunities for new voices and perspectives in both sectors.

    Critics argue that the revolving door can also undermine public trust in government and increase the risk of corruption, as the movement of individuals between sectors can blur the lines between public service and private gain. However, defenders of the revolving door suggest that it can facilitate the exchange of expertise and ideas between the public and private sectors, and that individuals with experience in both sectors may be better equipped to make informed policy decisions.
    """
    def __init__(self):
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def get_people_in_sector(self, sector):
        return [person for person in self.people if person.sector == sector]

    def get_all_people(self):
        return self.people

    def __str__(self):
        return "\n".join([str(person) for person in self.people])
