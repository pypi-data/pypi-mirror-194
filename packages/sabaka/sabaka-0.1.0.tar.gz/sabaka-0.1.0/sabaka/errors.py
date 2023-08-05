"""
errors: subclasses adding error message functionality to base exceptions
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2023, Corey Rayburn Yung
License: Apache-2.0

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Contents:

      
ToDo:


"""
from __future__ import annotations
from collections.abc import Callable, Iterable
import inspect
from typing import Any, Optional, Type

from . import base
from . import configuration 

    
class ImportFailed(base.DynamicMessage, ImportError):
    """Error for a failed module importation.
    
    Attributes:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to the default value stored in the corresponding 
            configuration module of sabaka.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.DEFAULT_IMPORT
        
    def compose(
        self, 
        item: str, 
        importer: Optional[Callable | str] = None) -> str:
        """Constructs an error message based on passed arguments.

        Args:
            item (Any): item that failed the validation check.
            importer (Optional[Callable | str]): importer callable or the str 
                name of the importer. Defaults to None.
        
        Returns:
            str: error message created from passed arguments
            
        """
        item_name = configuration.NAMER(item)
        importer_name = configuration.NAMER(importer)
        if importer is None:
            return f'{item_name} failed to import'
        else:
            return f'{item_name} failed to import using {importer_name}'
        
        
class NotAttribute(base.DynamicMessage, AttributeError):
    """Error for a missing class or instance attribute.
    
    Attributes:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to the default value stored in the corresponding 
            configuration module of sabaka.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.DEFAULT_ATTRIBUTE
        
    def compose(self, base: Any, attribute: str) -> str:
        """Returns an error message based on passed arguments.

        Args:
            item (Any): item of which 'attribute' was found not be an attribute.
            attribute (str): name that was found not to be an attribute of 
                'item'.
        
        Returns:
            str: error message created from passed arguments
            
        """
        base_name = configuration.NAMER(base)
        if inspect.isclass(base):
            return f'{base_name} has no attribute named "{attribute}"'  
        else:  
            return (
                f'The {base_name} instance has no attribute named '
                f'"{attribute}"') 


class NotType(base.DynamicMessage, TypeError):
    """Error for a type check failure.
    
    Attributes:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to the default value stored in the corresponding 
            configuration module of sabaka.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.DEFAULT_TYPE
    
    def compose(self, item: Any, kind: Type[Any] | str) -> str:
        """Returns an error message based on passed arguments.

        Args:
            item (Any): item or name of the item that failed the type check.
            kind (Type[Any] | str): type or name of the type against which 
                'item' was checked.
        
        Returns:
            str: error message created from passed arguments
            
        """
        kind_name = configuration.NAMER(kind)
        item_name = configuration.NAMER(item)
        return f'{item_name} is not a {kind_name}'
    

class OutOfRange(base.DynamicMessage, IndexError):
    """Error for an iterable out of range.
    
    Attributes:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to the default value stored in the corresponding 
            configuration module of sabaka.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.DEFAULT_RANGE
    
    def compose(self, item: Iterable, index: int) -> str:
        """Returns an error message based on passed arguments.

        Args:
            item (Iterable): iterable that is out of range.
            index (int): the value of the index which created the error.
        
        Returns:
            str: error message created from passed arguments
            
        """
        item_name = configuration.NAMER(item)
        if index >= 0:
            return (
                f'The index of {item_name} is at {index}, above the maximum '
                f'allowable index of {len(item) - 1}')
        else:
            return (
                f'The index of {item_name} is at {index}, below the minimum '
                f'allowable index of {-1 * len(item)}')
    
        
class ValidationFailed(base.DynamicMessage, AttributeError):
    """Error for a failed check by a passed callable.
    
    Attributes:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to the default value stored in the corresponding 
            configuration module of sabaka.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.DEFAULT_VALIDATION
        
    def compose(
        self, 
        item: Any, 
        validator: Optional[Callable | str] = None) -> str:
        """Constructs an error message based on passed arguments.

        Args:
            item (Any): item that failed the validation check.
            validator (Optional[Callable | str]): validator callable or the str 
                name of the validator. Defaults to None.
        
        Returns:
            str: error message created from passed arguments
            
        """
        item_name = configuration.NAMER(item)
        if validator is None:
            return f'{item_name} failed a validation check'
        else:
            validator_name = configuration.NAMER(validator)
            return f'{item_name} failed a validation check by {validator_name}'
         