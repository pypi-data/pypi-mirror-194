"""
base: exception mixins
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
    ComposedMessage (abc.ABC): Mixin supporting an error message based on passed 
        arguments.
    DefaultMessage (abc.ABC): Mixin supporting a default error message if one is 
        not passed.
    DynamicMessage (abc.ABC): Mixin supporting constructed and default error 
        messages, combining the functionality of ComposedMessage and 
        DefaultMessage.
      
ToDo:


"""
from __future__ import annotations
import abc
from typing import Any

from . import configuration 


class ComposedMessage(abc.ABC):
    """Mixin supporting an error message based on passed arguments.
    
    This mixin prioritizes how the loggged error message is constructed in the
    following order:
        1) passed message;
        2) message created by other passed arguments using the 'compose' 
            method, if any args or kwargs are passed;
        3) whatever message is created be the parent or mixed-in Exception 
            subclass's '__init__' method when no message is passed.
        
    """
    
    def __init__(self, *args: Any, **kwargs: Any):
        """Calls the mixed-in Exception class with the appropriate message."""
        if (args and isinstance(list(args)[0], str)) and not kwargs:
            super().__init__(*args, **kwargs)
        elif args or kwargs:
            super().__init__(self.compose(*args, **kwargs))
        else:
            super().__init__()
            
    def compose(self, *args, **kwargs) -> str:
        """Constructs an error message based on passed arguments.
        
        Subclasses should override this method. But, in the event this method
        is not overridden, a str is returned of the passed args and arguments of
        kwargs.
        
        In order for this method to be called and work correctly, the first
        parameter may NOT be a str type. If it is, the '__init__' method will
        assume that str is an error message and the 'compose' method will never
        be called.
        
        Return:
            str: created from args and kwargs.
            
        """
        return ', '.join([str(args), str(kwargs.values())])
   
   
class DefaultMessage(abc.ABC):
    """Mixin supporting a default error message if one is not passed.
    
    This mixin prioritizes how the loggged error message is constructed in the
    following order:
        1) passed message;
        2) message in the class 'default' attribute;
        3) whatever message is created be the parent or mixed-in Exception 
            subclass's '__init__' method when no message is passed.
   
    Attributes:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to configuration.MISSING.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.MISSING
    
    def __init__(self, *args: Any, **kwargs: Any):
        """Calls the mixed-in Exception class with the appropriate message."""
        if len(*args) > 0 and isinstance(list(*args)[0], str):
            super().__init__(*args, **kwargs)
        elif self.default is not configuration.MISSING:
            super().__init__(self.default)
        else:
            super().__init__()
   
   
class DynamicMessage(abc.ABC):
    """Mixin supporting constructed and default error messages.
    
    This mixin provides sources of alternative or default error messages if one
    is not directly passed to a Exception subclass. If a message is passed, the 
    Exception class will operate in the same manner as a normal exception.
    
    This mixin prioritizes how the loggged error message is constructed in the
    following order:
        1) passed message;
        2) message created by other passed arguments using the 'compose' 
            method, if any args or kwargs are passed;
        3) message in the class 'default' attribute;
        4) whatever message is created be the parent or mixed-in Exception 
            subclass's '__init__' method when no message is passed.
   
    Attributes:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to configuration.MISSING.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.MISSING
    
    def __init__(self, *args: Any, **kwargs: Any):
        """Calls the mixed-in Exception class with the appropriate message."""
        if (args and isinstance(list(args)[0], str)) and not kwargs:
            super().__init__(*args, **kwargs)
        elif args or kwargs:
            super().__init__(self.compose(*args, **kwargs))
        elif self.default is not configuration.MISSING:
            super().__init__(self.default)
        else:
            super().__init__()
            
    def compose(self, *args, **kwargs) -> str:
        """Constructs an error message based on passed arguments.
        
        Subclasses should override this method. But, in the event this method
        is not overridden, a str is returned of the passed args and arguments of
        kwargs.
        
        In order for this method to be called and work correctly, the first
        parameter may NOT be a str type. If it is, the '__init__' method will
        assume that str is an error message and the 'compose' method will never
        be called.
                
        Returns:
            str: created from args and kwargs.
            
        """
        return ', '.join([str(args), str(kwargs.values())])
   