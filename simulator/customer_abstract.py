from mesa import Agent
from abc import ABCMeta, abstractmethod


class AbstractCustomer(Agent,  metaclass=ABCMeta):
    def __init__(self, unique_id, transaction_model, fraudster):
        """
        Abstract class for customers, which can either be genuine or fraudulent.
        :param unique_id:           the (unique) customer ID
        :param transaction_model:   the transaction model that is used, instance of mesa.Model
        :param fraudster:           boolean whether customer is genuine or fraudulent
        """
        # call super init from mesa agent
        super().__init__(unique_id, transaction_model)

        # each customer has to say if it's a fraudster or not
        self.fraudster = int(fraudster)

        # pick country, currency, card
        self.country = self.initialise_country()
        self.currency = self.initialise_currency()
        self.card_id = self.initialise_card_id()

        # variable for whether a transaction is currently being processed
        self.active = False

        # fields for storing the current transaction properties
        self.curr_merchant = None
        self.curr_amount = None

        # variable tells us whether the customer wants to stay after current transaction
        self.stay = True

    def step(self):
        """ 
        This is called in each simulation step (i.e., one hour).
        Each individual customer/fraudster decides whether to make a transaction or  not.
        """
        if self.decide_making_transaction():
            self.active = True
            self.make_transaction()
            self.stay_customer()
        else:
            self.active = False
            self.curr_merchant = None
            self.curr_amount = None

    @abstractmethod
    def initialise_country(self):
        """
        Select country where customer's card was issued
        :return:    country
        """
        pass

    @abstractmethod
    def initialise_currency(self):
        """
        Select currency in which customer makes transactions
        :return:    string
        """
        pass

    @abstractmethod
    def initialise_card_id(self):
        """ 
        Select creditcard number (unique ID) for customer
        :return:    credit card number
        """
        pass

    @abstractmethod
    def decide_making_transaction(self):
        """
        Decide whether to make transaction or not, given the current time step
        :return:    Boolean indicating whether to make transaction or not
        """
        pass

    @abstractmethod
    def make_transaction(self):
        """
        Make a transaction. Should update these variables:
            self.curr_merchant, self.curr_transaction_amount
        """
        pass

    @abstractmethod
    def stay_customer(self):
        """ 
        At a given point in time, decide whether or not to make another transaction in the future.
        :return:    Boolean indicating whether to make another transaction (stay=True) or not
        """
        pass
