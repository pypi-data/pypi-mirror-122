"""Module that contains the SAM learner code for single agent problems."""
import logging
from pathlib import Path
from typing import List, Optional, NoReturn, Dict

from pddl.pddl import Domain, Action, Effect
from pyperplan import Parser

from sam_learner.core import PredicatesMatcher, extract_effects
from sam_learner.sam_models import GroundedAction, State, TrajectoryComponent, Trajectory, Mode


class SAMLearner:
	"""Class that represents the safe action model learner algorithm."""

	logger: logging.Logger
	working_directory_path: Path
	trajectories: List[Trajectory]
	learned_domain: Domain
	matcher: PredicatesMatcher
	known_actions: Dict[str, Action]

	def __init__(
			self, working_directory_path: Optional[str] = None, domain_file_name: str = "domain.pddl", mode: Mode = "production",
			domain: Optional[Domain] = None, known_actions: Dict[str, Action] = {}):
		self.logger = logging.getLogger(__name__)
		self.known_actions = known_actions
		if mode == "development":
			self.matcher = PredicatesMatcher(domain=domain)
			self.learned_domain = domain
			return

		self.working_directory_path = Path(working_directory_path)
		domain_path = self.working_directory_path / domain_file_name
		self.learned_domain = Parser(domain_path).parse_domain(read_from_file=True)
		self.learned_domain.actions = {}
		self.matcher = PredicatesMatcher(domain_path=str(domain_path))
		if known_actions is not None:
			self.learned_domain.actions = {
				name: action for name, action in known_actions.items()
			}

	def handle_action_effects(
			self, grounded_action: GroundedAction, previous_state: State, next_state: State) -> Effect:
		"""Finds the effects generated from the previous and the next state on this current step.

		:param grounded_action: the grounded action that was executed according to the trajectory.
		:param previous_state: the state that the action was executed on.
		:param next_state: the state that was created after executing the action on the previous
			state.
		:return: the effect containing the add and del list of predicates.
		"""
		grounded_add_effects, grounded_del_effects = extract_effects(previous_state, next_state)
		action_effect = Effect()
		action_effect.addlist = action_effect.addlist.union(self.matcher.get_possible_literal_matches(
			grounded_action, grounded_add_effects))
		action_effect.dellist = action_effect.dellist.union(self.matcher.get_possible_literal_matches(
			grounded_action, grounded_del_effects))
		return action_effect

	def add_new_action(
			self, grounded_action: GroundedAction, previous_state: State, next_state: State) -> NoReturn:
		"""Create a new action in the domain.

		:param grounded_action: the grounded action that was executed according to the trajectory.
		:param previous_state: the state that the action was executed on.
		:param next_state: the state that was created after executing the action on the previous
			state.
		"""
		self.logger.info(f"Adding the action {grounded_action.activated_action_representation} "
						 f"to the domain.")
		new_action = Action(name=grounded_action.lifted_action_name,
							signature=grounded_action.lifted_signature,
							precondition=[],
							effect=None)

		# adding the preconditions each predicate is grounded in this stage.
		possible_preconditions = self.matcher.get_possible_literal_matches(grounded_action,
																		   previous_state.facts)
		new_action.precondition = list(set(possible_preconditions))

		action_effect = self.handle_action_effects(grounded_action, previous_state, next_state)
		new_action.effect = action_effect
		self.learned_domain.actions[new_action.name] = new_action
		self.logger.debug(
			f"Finished adding the action {grounded_action.activated_action_representation}.")

	def update_action(self, grounded_action: GroundedAction, previous_state: State,
					  next_state: State) -> NoReturn:
		"""Create a new action in the domain.

		:param grounded_action: the grounded action that was executed according to the trajectory.
		:param previous_state: the state that the action was executed on.
		:param next_state: the state that was created after executing the action on the previous
			state.
		"""
		action_name = grounded_action.lifted_action_name
		self.logger.info(f"Updating the action - {action_name}")
		if action_name in self.known_actions:
			self.logger.debug(f"The action {action_name} is already known to the agent. Skipping!")
			return

		current_action: Action = self.learned_domain.actions[action_name]
		model_preconditions = current_action.precondition.copy()
		possible_preconditions = self.matcher.get_possible_literal_matches(
			grounded_action, previous_state.facts)

		for precondition in model_preconditions:
			if precondition not in possible_preconditions:
				current_action.precondition.remove(precondition)

		action_effect: Effect = self.handle_action_effects(
			grounded_action, previous_state, next_state)
		current_action.effect.addlist = current_action.effect.addlist.union(action_effect.addlist)
		current_action.effect.dellist = current_action.effect.dellist.union(action_effect.dellist)
		self.logger.debug(f"Done updating the action - {grounded_action.lifted_action_name}")

	def handle_single_trajectory_component(self, component: TrajectoryComponent) -> NoReturn:
		"""Handles a single trajectory component as a part of the learning process.

		:param component: the trajectory component that is being handled at the moment.
		"""
		previous_state = component.previous_state
		grounded_action = component.grounded_action
		next_state = component.next_state
		if grounded_action.lifted_action_name not in self.learned_domain.actions:
			self.add_new_action(grounded_action, previous_state, next_state)

		else:
			self.update_action(grounded_action, previous_state, next_state)

	def learn_action_model(self, trajectories: List[Trajectory]) -> Domain:
		"""Learn the SAFE action model from the input trajectories.

		:param trajectories: the list of trajectories that are used to learn the safe action model.
		:return: a domain containing the actions that were learned.
		"""
		# First making sure that the domain doesn't have any actions.
		self.logger.info("Starting to learn the action model!")
		for trajectory in trajectories:
			for component in trajectory:
				self.handle_single_trajectory_component(component)

		return self.learned_domain
