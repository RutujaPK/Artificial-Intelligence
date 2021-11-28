import read
import copy
from util import *
from logical_classes import *

verbose = 0


class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ###################################################
        type = fact_or_rule.name  # Check if the given type is a fact or a rule

        if type == 'fact':  # if its a fact
            # get the fact and creating a supporting array for the same
            fact = self._get_fact(fact_or_rule)
            support_array = fact.supports_facts  # supporting array created

            for supported_rule in fact.supports_rules:  # for every supported_rule in the array
                for supporting_fact in supported_rule.supported_by:  # for every supporting fact in the array
                    # if supporting fact at index 0 is the fact we retrieved, them
                    if (supporting_fact[0] == fact):
                        supported_rule.supported_by.remove(
                            supporting_fact)  # we remove the supporting fact
                # if length of array is not 0 or the condition asserted is not true, then
                if (len(supported_rule.supported_by) == 0 and supported_rule.asserted != True):
                    # we keep on recurssively implementing the retract function
                    self.kb_retract(supported_rule)

            for supported_fact in support_array:    # for every supported_fact in the array
                for supporting_fact in supported_fact.supported_by:  # for every supporting fact in the array
                    # if supporting fact at index 0 is the fact we retrieved, them
                    if (supporting_fact[0] == fact):
                        supported_fact.supported_by.remove(
                            supporting_fact)  # we remove the supporting fact
                # if length of array is not 0 or the condition asserted is not true, then
                if (len(supported_fact.supported_by) == 0 and supported_fact.asserted != True):
                    # we keep on recurssively implementing the retract function
                    self.kb_retract(supported_fact)

            # if length of array is not 0 or the condition asserted is not true, then
            if (len(fact.supported_by) == 0 and fact.asserted != True):
                self.facts.remove(fact)  # we remove the fact from the array

        if type == 'rule':  # if its a fact
            rule = self._get_rule(fact_or_rule)  # get the rule
            # if length of array is not 0 or the condition asserted is not true, then
            if (len(rule.supported_by) == 0 and rule.asserted != True):

                for supported_rule in rule.supports_rules:  # for every supported_rule in the array
                    for supporting_rule in supported_rule.supported_by:  # for every supporting_rule in the array
                        # if supporting rule at index 1 is the rule we retrieved, them
                        if (supporting_rule[1] == rule):
                            supported_rule.supported_by.remove(
                                supporting_rule)  # we remove the supporting rule
                    # if length of array is not 0 or the condition asserted is not true, then
                    if (len(supported_rule.supported_by) == 0 and supported_rule.asserted != True):
                        # we keep on recurssively implementing the retract function
                        self.kb_retract(supported_rule)

                for supported_fact in rule.supports_facts:
                    for supporting_rule in supported_fact.supported_by:
                        # if supporting rule at index 1 is the rule we retrieved, them
                        if (supporting_rule[1] == rule):
                            supported_fact.supported_by.remove(
                                supporting_rule)  # we remove the supporting rule
                    # if length of array is not 0 or the condition asserted is not true, then
                    if (len(supported_fact.supported_by) == 0 and supported_fact.asserted != True):
                        # we keep on recurssively implementing the retract function
                        self.kb_retract(supported_fact)

                self.rules.remove(rule)  # we remove the rule from the array


class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """

        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
               [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # creating a variable to match all possible bindings
        possible_bindings = match(fact.statement, rule.lhs[0])
        # variable that maintains the array length
        array_length = len(rule.lhs)

        # If the possible binding is true and the length of array is 1, then
        if possible_bindings != False and array_length == 1:

            # create and instantiate my_right_hand_side variable
            right_hand_side = instantiate(rule.rhs, possible_bindings)
            support = [[fact, rule]]  # create a support variable
            my_fact = Fact(right_hand_side, support)
            fact_array = fact.supports_facts
            rule_array = rule.supports_facts
            rule_array.append(my_fact)
            fact_array.append(my_fact)
            kb.kb_add(my_fact)

        # If the possible binding is true and the length of array is greater than 1, then
        elif possible_bindings != False and array_length > 1:

            # create and instantiate my_right_hand_side variable
            right_hand_side = instantiate(rule.rhs, possible_bindings)
            support = [[fact, rule]]  # create a support variable
            left_hand_side = []
            helper = rule.lhs[1:array_length]

            for element in helper:
                instance = instantiate(element, possible_bindings)
                left_hand_side.append(instance)

            rule_helper = [left_hand_side, right_hand_side]
            my_rule = Rule(rule_helper, support)
            fact_array = fact.supports_rules
            rule_array = rule.supports_rules
            rule_array.append(my_rule)
            fact_array.append(my_rule)
            kb.kb_add(my_rule)
