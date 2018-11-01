"""
Choice field choices
"""

from djchoices import DjangoChoices, ChoiceItem


class DocumentCategory(DjangoChoices):
    """Press+Bill category"""
    act_amendment = ChoiceItem(0, "Novela zákona")
    bill = ChoiceItem(1, "Návrh nového zákona")
    other = ChoiceItem(2, "Iný typ")
    petition = ChoiceItem(3, "Petícia")
    international_treaty = ChoiceItem(4, "Medzinárodná zmluva")
    report = ChoiceItem(5, "Správa")
    constitutional_law = ChoiceItem(6, "Ústavný zákon")
    information = ChoiceItem(7, "Informácia")
    budget_law = ChoiceItem(8, "Návrh zákona o štátnom rozpočte")
    presidential_veto = ChoiceItem(9, "Zákon vrátený prezidentom")
