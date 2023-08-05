# import abc
# from typing import Dict, Optional
#
# from django.db import models
#
# from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
# from django_graphene_crud_generator.crud_generator.contexts import CRUDBuildContext, CRUDRuntimeContext
# from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneReturnType
#
#
# class CreateMutationReturnTrueMixIn:
#
#     def _get_mutation_success_return_name(self, context: CRUDBuildContext) -> str:
#         return "ok"
#
#     def _create_mutation_return_value(self, context: CRUDBuildContext) -> Dict[str, TGrapheneReturnType]:
#         result = dict()
#         flag_name = self._get_mutation_success_return_name(context)
#         result[flag_name] = GraphQLHelper.return_ok()
#         return result
#
#     def get_ok_flag_name(self, runtime_context: CRUDRuntimeContext):
#         return list(
#             filter(lambda x: self._get_mutation_success_return_name(runtime_context.build_context).lower() in x.lower(),
#                    runtime_context.build_context.create_return_value.keys()))[0]
#
#     def _create_generate_mutation_instance_row_already_exists(self, mutation_class: type,
#                                                               item_in_db: Optional[models.Model], runtime_context: CRUDRuntimeContext) -> any:
#         flag_name = self.get_ok_flag_name(runtime_context)
#         return mutation_class(**{flag_name: False})
#
#     def _create_generate_mutation_instance_row_added(self, mutation_class: type, result: any,
#                                                      runtime_context: CRUDRuntimeContext) -> any:
#         flag_name = self.get_ok_flag_name(runtime_context)
#         return mutation_class(**{flag_name: True})
