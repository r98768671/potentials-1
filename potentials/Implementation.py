# coding: utf-8
# Standard libraries
import uuid
import datetime

# https://github.com/usnistgov/DataModelDict
from DataModelDict import DataModelDict as DM

# Local imports
from .tools import aslist
from .Artifact import Artifact
from .Parameter import Parameter
from .WebLink import WebLink

class Implementation():
    """
    Class for representing Implementation metadata records.
    records.
    """
    def __init__(self, model=None, type=None, key=None,
                 id=None, status=None, date=None, notes=None,
                 artifacts=None, parameters=None, weblinks=None):
        """
        Parameters
        ----------
        model : str or DataModelDict, optional
            Model content or file path to model content.
        type
        key
        id
        status
        date
        notes
        artifacts
        parameters
        weblinks
        """
        if model is not None:
            # Load existing record
            try:
                assert type is None
                assert key is None
                assert id is None
                assert status is None
                assert date is None
                assert notes is None
                assert artifacts is None
                assert parameters is None
                assert weblinks is None
            except:
                raise TypeError('model cannot be given with any other parameter')
            else:
                self.load(model)
        else:
            # Build new record
            self.type = type
            self.key = key
            self.id = id
            self.status = status
            self.date = date
            self.notes = notes
            
            self.artifacts = []
            if artifacts is not None:
                for artifact in aslist(artifacts):
                    self.add_artifact(**artifact)
            
            self.parameters = []
            if parameters is not None:
                for parameter in aslist(parameters):
                    self.add_parameter(**parameter)
            
            self.weblinks = []
            if weblinks is not None:
                for weblink in aslist(weblinks):
                    self.add_weblink(**weblink)

    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, v):
        if v is None:
            self.__type = None
        else:
            self.__type = str(v)

    @property
    def key(self):
        return self.__key
    
    @key.setter
    def key(self, v):
        if v is None:
            self.__key = str(uuid.uuid4())
        else:
            self.__key = str(v)
            
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, v):
        if v is None:
            self.__id = None
        else:
            self.__id = str(v)

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, v):
        if v is None:
            self.__status = 'active'
        else:
            self.__status = str(v)

    @property
    def date(self):
        return self.__date
    
    @date.setter
    def date(self, v):
        if v is None:
            self.__date = datetime.date.today()
        elif isinstance(v, datetime.date):
            self.__date = v
        elif isinstance(v, str):
            self.__date = datetime.datetime.strptime(v, '%Y-%m-%d').date()
        else:
            raise TypeError('Invalid date type')
    
    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, v):
        if v is None:
            self.__notes = None
        else:
            self.__notes = str(v)

    def html(self):
        """Returns an HTML representation of the object."""
        
        htmlstr = ''
        
        htmlstr += f'<b>{self.type}</b> ({self.id})<br/>\n'
        if self.status != 'active':
            htmlstr += f'<b>{self.status}</b><br/>\n'
        
        if self.notes is not None:
            htmlstr += f'<b>Notes:</b> {self.notes}</br>\n'
        
        if len(self.artifacts) > 0:
            htmlstr += '<b>Files:</b><br/>\n'
            for artifact in self.artifacts:
                htmlstr += f'{artifact.html()}<br/>\n'
        
        if len(self.parameters) > 0:
            htmlstr += '<b>Parameters:</b><br/>\n'
            for parameter in self.parameters:
                htmlstr += f'{parameter.html()}<br/>\n'
        
        if len(self.weblinks) > 0:
            htmlstr += '<b>Links:</b><br/>\n'
            for weblink in self.weblinks:
                htmlstr += f'{weblink.html()}<br/>\n'
        
        return htmlstr

    def load(self, model):
        """
        Loads the object info from data model content
        
        Parameters
        ----------
        model : str or DataModelDict
            Model content or file path to model content.
        """
        model = DM(model)
        imp = model.find('implementation')
        self.key = imp['key']
        self.id = imp.get('id', None)
        self.status = imp.get('status', None)
        self.date = imp.get('date', None)
        self.type = imp.get('type', None)
        if 'notes' in imp:
            self.notes = imp['notes']['text']
        else:
            self.notes = None

        self.artifacts = []
        for artifact in imp.iteraslist('artifact'):
            self.add_artifact(model=DM([('artifact', artifact)]))

        self.parameters = []
        for parameter in imp.iteraslist('parameter'):
            self.add_parameter(model=DM([('parameter', parameter)]))

        self.weblinks = []
        for weblink in imp.iteraslist('web-link'):
            self.add_weblink(model=DM([('web-link', weblink)]))

    def asdict(self):
        """Returns a flat dict representation of the object"""
        data = {}
        
        # Copy class attributes to dict
        data['key'] = self.key
        data['id'] = self.id
        data['date'] = self.date
        data['status'] = self.status
        data['notes'] = self.notes
        data['type'] = self.type
        data['artifacts'] = self.artifacts
        data['parameters'] = self.parameters
        data['weblinks'] = self.weblinks
        
        return data

    def asmodel(self):
        """
        Returns the object info as data model content
        
        Returns
        ----------
        DataModelDict: The data model content.
        """

        model = DM()
        model['implementation'] = imp = DM()
        imp['key'] = self.key
        if self.id is not None:
            imp['id'] = self.id
        imp['status'] = self.status
        imp['date'] = str(self.date)
        if self.type is not None:
            imp['type'] = self.type
        if self.notes is not None:
            imp['notes'] = DM([('text', self.notes)])
        for artifact in self.artifacts:
            imp.append('artifact', artifact.asmodel()['artifact'])
        for parameter in self.parameters:
            imp.append('parameter', parameter.asmodel()['parameter'])
        for weblink in self.weblinks:
            imp.append('web-link', weblink.asmodel()['web-link'])
        
        return model

    def add_artifact(self, model=None, filename=None, label=None, url=None):
        self.artifacts.append(Artifact(model=model, filename=filename, label=label, url=url))

    def add_weblink(self, model=None, url=None, label=None, linktext=None):
        self.weblinks.append(WebLink(model=model, url=url, label=label, linktext=linktext))

    def add_parameter(self, model=None, name=None, value=None, unit=None):
        self.parameters.append(Parameter(model=model, name=name, value=value, unit=unit))
