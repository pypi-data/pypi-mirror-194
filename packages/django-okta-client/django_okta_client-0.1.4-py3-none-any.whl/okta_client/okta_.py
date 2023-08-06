#!python
'''Configuration module for standalone django-okta-client
Configuration parameters for a test deployment of django-okta-client.
'''

import logging

import asgiref.sync
import datetime
import okta.client

from django.conf import settings
from django.db import models

LOGGER = logging.getLogger(__name__)


class OktaClientError(RuntimeError):
	'''Okta Client Error
	Exception type for Okta SDK Client sourced errors.
	'''
	pass


class OktaClientMixin:
	'''Okta SDK Client
	Simplify the use of the Okta SDK client. It's expected for a "OKTA_CLIENT_SDK" dict value to exist in the Django settings. It's passed as is to the client https://github.com/okta/okta-sdk-python#configuration-reference
	'''

	def __getattr__(self, name):
		'''Lazy instantiation
		Some computation that is left pending until is needed.
		'''

		if name == '_okta_client':
			value = okta.client.Client(settings.OKTA_CLIENT_SDK)
		else:
			return getattr(super(), name)

		self.__setattr__(name, value)
		return value

	def okta_client_call(self, method_name, *args, **kwargs):
		'''Magic call
		Perform an API call. It converts the calls to sync (from the native async methods)
		and pull all the pages, for paginated requests. It also triggers Exceptions from errors returned.
		'''

		result = asgiref.sync.async_to_sync(getattr(self._okta_client, method_name))(*args, **kwargs)

		if len(result) == 3:
			result, response, err = result
		elif len(result) == 2:
			response, err = result
		else:
			raise RuntimeError('Unknown result: {}'.format(result))
		if err is not None:
			raise OktaClientError(err)
		while response.has_next():
			partial, err = asgiref.sync.async_to_sync(response.next)()
			if err is not None:
				raise OktaClientError(err)
			result.extend(partial)
		return result


class OktaModelProfileSyncMixin:
	'''Okta Model Profile Sync

	'''

	@classmethod
	def _attributes_from_okta_profile(cls, okta_profile):
		attributes = {}
		for field in cls._meta.fields:
			if hasattr(okta_profile, field.name):
				okta_attr = getattr(okta_profile, field.name)
				if (okta_attr is None) or not len(okta_attr):
					continue
				if isinstance(field, models.fields.DateTimeField):
					okta_attr = datetime.datetime.fromisoformat(okta_attr.rstrip('Z'))
				attributes[field.name] = okta_attr
		return attributes

	@classmethod
	def from_okta_profile(cls, okta_profile):
		return cls(**cls._attributes_from_okta_profile(okta_profile))

	def update_from_okta_profile(self, okta_profile):
		for field_name, field_value in self._attributes_from_okta_profile(okta_profile).items():
			setattr(self, field_name, field_value)
		return self

