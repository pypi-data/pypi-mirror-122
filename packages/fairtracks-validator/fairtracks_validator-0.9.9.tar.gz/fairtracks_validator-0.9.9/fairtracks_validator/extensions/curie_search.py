#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rfc3987
import uritools
from jsonschema.exceptions import FormatError, ValidationError

from extended_json_schema_validator.extensions.abstract_check import AbstractCustomFeatureValidator
from .curie_cache import CurieCache, Curie

import logging
import re
import xdg
import os, sys
import tempfile
import shutil
import atexit

class CurieSearch(AbstractCustomFeatureValidator):
	VALID_MATCHES = {
		'canonical': None,
		'loose': None,
		'basic': None
	}
	
	FormatName = 'curie'
	KeyAttributeName = 'namespace'
	MatchTypeAttrName = 'matchType'
	
	def __init__(self, schemaURI, jsonSchemaSource='(unknown)', config={}, isRW=True):
		super().__init__(schemaURI, jsonSchemaSource, config, isRW=isRW)
	
	@property
	def triggerAttribute(self):
		return self.KeyAttributeName
	
	@property
	def triggerJSONSchemaDef(self):
		return {
			self.triggerAttribute : {
				"oneOf": [
					{
						"type": "string"
					}
					,
					{
						"type": "array",
						"items": {
							"type": "string",
							"minLength": 1
						},
						"minItems": 1
					}
				]
			},
			self.MatchTypeAttrName : {
				"type": "string",
				"enum": list(self.VALID_MATCHES.keys())
			}
		}
	
	@property
	def needsBootstrapping(self):
		return False
	
	def invalidateCaches(self):
		self.InvalidateCurieCache(cachePath=self.config.get('cacheDir'))
	
	def warmUpCaches(self):
		cache = self.GetCurieCache(cachePath=self.config.get('cacheDir'), warmUp=self.isRW)
	
	@classmethod
	def InvalidateCurieCache(cls, cachePath=None):
		if hasattr(cls,'CurieCache'):
			cache = getattr(cls,'CurieCache')
			delattr(cls,'CurieCache')
			cache.invalidate()
			del cache
		
		cachePath = cls.GetCurieCachePath(cachePath=cachePath)
		delattr(cls,'CurieCachePath')
		shutil.rmtree(cachePath,ignore_errors=True)
	
	def isValid(self,validator,nslist,origValue,schema):
		found = False
		checkedPatterns = []
		matchType = str(schema.get(self.MatchTypeAttrName,'loose'))  if schema is not None  else 'canonical'
		if matchType not in CurieSearch.VALID_MATCHES:
			raise ValidationError("attribute '{0}' is {1} but it must be one of the next values: {2}".format(self.MatchTypeAttrName,matchType,CurieSearch.VALID_MATCHES.keys()))
		
		cache = self.GetCurieCache(cachePath=self.config.get('cacheDir'), warmUp=self.isRW)
		
		parsed = None
		try:
			parsed = rfc3987.parse(origValue, rule="URI")
		except BaseException as be:
			if matchType != 'loose':
				raise be
		# Trying to decide the matching mode
		prefix = None
		if parsed:
			prefix = parsed.get('scheme')
			if prefix:
				if len(prefix) > 0:
					if matchType == 'loose':
						matchType = 'canonical'
					
					# We have to enforce lowercase schemes
					if prefix.lower() != prefix:
						raise ValidationError('The namespace of {} must be in lower case'.format(origValue))
		
		if nslist:
			# The restricted namespaces list could have some of them in capitals
			l_nslist = list(map(lambda x: None  if x is None  else x.lower()  if isinstance(x,str)  else str(x).lower(), nslist))
		else:
			l_nslist = nslist
		
		if matchType == 'basic':
			# Basic mode is like canonical, but without querying identifiers.org cache
			found = l_nslist and (prefix in l_nslist)
		elif matchType == 'loose':
			if l_nslist:
				valToVal = origValue
				validatedCURIEs = list(filter(lambda curie: curie is not None,map(lambda namespace: cache.get(namespace),l_nslist)))
				if not validatedCURIEs:
					raise ValidationError('No namespace from {} was found in identifiers.org cache'.format(nslist))
				
				# Looking for a match
				for curie in validatedCURIEs:
					checkedPatterns.append(curie.pattern)
					pat = re.compile(curie.pattern)
					if pat.search(valToVal):
						found = True
						break
			else:
				raise ValidationError('In "loose" mode, at least one namespace must be declared')
		elif prefix is None:
			raise ValidationError('In "canonical" mode, the value must be prefixed by the namespace')
		else:
			# Searching in canonical mode. To do that, we have to remove the prefix
			valToVal = origValue[(origValue.find(':')+1):]
			# The case where the namespace list is empty
			if l_nslist and (prefix not in l_nslist):
				raise ValidationError('The namespace {} is not in the list of the accepted ones: {}'.format(prefix,nslist))
			
			curie = cache.get(prefix)
			if not curie:
				raise ValidationError('The namespace {} was not found in identifiers.org cache'.format(prefix))
			
			checkedPatterns.append(curie.pattern)
			pat = re.compile(curie.pattern)
			found = pat.search(valToVal) or pat.search(origValue)
		
		return found, checkedPatterns
	
	@classmethod
	def GetCurieCachePath(cls, cachePath = None):
		if not hasattr(cls,'CurieCachePath'):
			doTempDir = False
			if cachePath is None:
				try:
					cachePath = xdg.BaseDirectory.save_cache_path('es.elixir.jsonValidator')
					# Is the directory writable?
					if not os.access(cachePath,os.W_OK):
						doTempDir = True
				except OSError as e:
					# As it was not possible to create the
					# directory at the cache path, create a
					# temporary directory
					doTempDir = True
			
			if doTempDir:
				# The temporary directory should be
				# removed when the application using this
				# class finishes
				#cachePath = tempfile.mkdtemp(prefix="curie", suffix="cache")
				#atexit.register(shutil.rmtree, cachePath, ignore_errors=True)
				cachePath = os.path.join(tempfile.gettempdir(),'cache_es.elixir.jsonValidator')
				os.makedirs(cachePath, exist_ok=True)
			
			setattr(cls,'CurieCachePath',cachePath)
		
		return getattr(cls,'CurieCachePath')
	
	@classmethod
	def GetCurieCache(cls, cachePath = None, warmUp=True):
		if cachePath is None:
			cachePath = cls.GetCurieCachePath(cachePath = cachePath)
		
		if not hasattr(cls,'CurieCache'):
			setattr(cls,'CurieCache',CurieCache(filename=os.path.join(cachePath,'CURIE_cache.sqlite3'), warmUp=warmUp))
		
		return getattr(cls,'CurieCache')
	
	@classmethod
	def IsCurie(cls,checker,instance):
		if isinstance(instance,Curie):
			return True
		
		if not isinstance(instance, str):
			return False
		
		parsed = rfc3987.parse(instance, rule="URI")
		if parsed and parsed.get('scheme'):
			cache = cls.GetCurieCache()
			curie = cache.get(parsed.get('scheme'))
			pat = re.compile(curie.pattern)
			return pat.search(instance[(instance.find(':')+1):])
		else:
			return False
	
	def validate(self,validator,namespace,value,schema):
		"""
		This method is here to be registered with custom validators
		"""
		# We do the validation only when the format is defined
		if (schema is None) or (schema.get("format") == self.FormatName):
			# Managing the different cases
			if namespace is None:
				nslist = []
			elif isinstance(namespace,list):
				nslist = namespace
			else:
				nslist = [ namespace ]
			
			try:
				# Now, let's check!
				validated, patterns = self.isValid(validator,nslist,value,schema)
				if not validated:
					yield ValidationError("Value '{0}' does not validate to any pattern ({1}) of the allowed schemes: {2}".format(value,'/'+'/, /'.join(patterns)+'/',', '.join(nslist)))
			except ValidationError as v:
				yield v
			except ValueError as ve:
				yield ValidationError("Unable to parse CURIE {0}: {1}".format(value,str(ve)))
			except BaseException as be:
				self.logger.exception("Unexpected error")
				yield ValidationError("Unexpected error: {}".format(str(be)))

	@classmethod
	def IsCorrectFormat(cls, value, schema = None):
		"""
		In empty context where the value is not a CURIE
		return true
		"""
		if schema and (':' in str(value)):
			curie = cls(None)
			for val in curie.validate(None,schema.get(cls.KeyAttributeName) if schema else None,value,schema):
				if isinstance(val,ValidationError):
					logging.error(val.message)
					return False
		return True
