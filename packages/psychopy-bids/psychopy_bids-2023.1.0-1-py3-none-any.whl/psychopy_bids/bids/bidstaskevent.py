"""This module provides a class to save your TaskEvents in the BIDS data structure"""


class BIDSTaskEvent(dict):
    """
    A BIDSTaskEvent describes timing and other properties of events recorded during a run.
    Events are, for example, stimuli presented to the participant or participant responses.

    Attributes
    ----------
    onset : int, float
        Onset (in seconds) of the event, measured from the beginning of the acquisition of the
        first data point stored in the corresponding task data file.
    duration : int, float, 'n/a'
        Duration of the event (measured from onset) in seconds.
    trial_type : str
        Primary categorisation of each trial to identify them as instances of the experimental
        conditions.
    sample : int
        Onset of the event according to the sampling scheme of the recorded modality.
    response_time : int, float, 'n/a'
        Response time measured in seconds.
    value : Any
        Marker value associated with the event.
    hed : str
        Hierarchical Event Descriptor (HED) Tag.
    stim_file : str
        Represents the location of the stimulus file (such as an image, video, or audio file)
        presented at the given onset time.
    identifier : str
        Represents the database identifier of the stimulus file presented at the given onset
        time.
    database : str
        Represents the database of the stimulus file presented at the given onset time.
    """

    def __init__(
        self,
        onset,
        duration,
        *arg,
        trial_type=None,
        sample=None,
        response_time=None,
        value=None,
        hed=None,
        stim_file=None,
        identifier=None,
        database=None,
        **kw,
    ):
        super().__init__(*arg, **kw)
        self.__dict__ = self
        self.onset = onset
        self.duration = duration
        self.trial_type = trial_type
        self.sample = sample
        self.response_time = response_time
        self.value = value
        self.hed = hed
        self.stim_file = stim_file
        self.identifier = identifier
        self.database = database

    # -------------------------------------------------------------------------------------------- #

    def __repr__(self):
        msg = "BIDSTaskEvent("
        for item in [item for item in self.__dict__.items() if item[1] is not None]:
            msg += f"{item[0].split('_BIDSTaskEvent__')[-1]}={item[1]}, "
        msg = msg[:-2] + ")"
        return msg

    # -------------------------------------------------------------------------------------------- #

    def from_dict(self, dictionary):
        """
        Converts a dictionary into a BIDSTaskEvent object.

        Parameters
        ----------
        dictionary : dict
            a dictionary representing a task event.

        Returns
        -------
        BIDSTaskEvent
            BIDSTaskEvent object representing all column names of a task event

        Examples
        --------
        >>> event = BIDSTaskEvent(0, 0)
        >>> event.from_dict({'onset': 1, 'duration': 1})
        BIDSTaskEvent(1, 1)
        """
        for key in dictionary.keys():
            setattr(self, key, dictionary[key])
        return self

    # -------------------------------------------------------------------------------------------- #

    def to_dict(self):
        """
        Converts a BIDSTaskEvent object to a dictionary.

        Returns
        -------
        dict
            Dictionary representing all column names of a task event

        Examples
        --------
        >>> BIDSTaskEvent(1, 1).to_dict()
        {'onset': 1, 'duration': 1, 'trial_type': None, 'sample': None, 'response_time': None,
        'value': None, 'hed': None, 'stim_file': None, 'identifier': None, 'database': None}
        """
        return {item[0].split("_BIDSTaskEvent__")[-1]: item[1] for item in self.items()}

    # -------------------------------------------------------------------------------------------- #

    @property
    def onset(self):
        """
        Onset (in seconds) of the event, measured from the beginning of the acquisition of the
        first data point stored in the corresponding task data file.
        """
        return self.__onset

    @onset.setter
    def onset(self, onset):
        if isinstance(onset, (int, float)):
            self.__onset = round(onset, 4)
        elif isinstance(onset, str):
            if onset.isnumeric():
                self.__onset = round(float(onset), 4)
            else:
                raise OnsetError(onset)
        else:
            raise OnsetError(onset)

    # -------------------------------------------------------------------------------------------- #

    @property
    def duration(self):
        """
        Duration of the event (measured from onset) in seconds.
        """
        return self.__duration

    @duration.setter
    def duration(self, duration):
        if isinstance(duration, str):
            if duration == "n/a":
                self.__duration = duration
            else:
                if duration.isnumeric():
                    self.__duration = round(float(duration), 4)
                else:
                    raise DurationError(duration)
        elif (isinstance(duration, (int, float))) and (duration >= 0):
            self.__duration = round(duration, 4)
        else:
            raise DurationError(duration)

    # -------------------------------------------------------------------------------------------- #

    @property
    def trial_type(self):
        """
        Primary categorisation of each trial to identify them as instances of the experimental
        conditions.
        """
        return self.__trial_type

    @trial_type.setter
    def trial_type(self, trial_type):
        if trial_type:
            if isinstance(trial_type, str):
                self.__trial_type = trial_type
            else:
                raise TrialTypeError(trial_type)
        else:
            self.__trial_type = None

    # -------------------------------------------------------------------------------------------- #

    @property
    def sample(self):
        """
        Onset of the event according to the sampling scheme of the recorded modality.
        """
        return self.__sample

    @sample.setter
    def sample(self, sample):
        if sample:
            if isinstance(sample, int):
                self.__sample = sample
            elif isinstance(sample, str):
                if sample.isnumeric():
                    self.__sample = int(sample)
                else:
                    raise SampleError(sample)
        else:
            self.__sample = None

    # -------------------------------------------------------------------------------------------- #

    @property
    def response_time(self):
        """
        Response time measured in seconds.
        """
        return self.__response_time

    @response_time.setter
    def response_time(self, response_time):
        if response_time:
            if isinstance(response_time, str):
                if response_time == "n/a":
                    self.__response_time = response_time
                else:
                    if response_time.isnumeric():
                        self.__response_time = round(float(response_time), 4)
                    else:
                        raise ResponseTimeError(response_time)
            elif isinstance(response_time, (int, float)):
                self.__response_time = round(response_time, 4)
            else:
                raise ResponseTimeError(response_time)
        else:
            self.__response_time = None

    # -------------------------------------------------------------------------------------------- #

    @property
    def value(self):
        """
        Marker value associated with the event.
        """
        return self.__value

    @value.setter
    def value(self, value):
        if value is not None:
            self.__value = value
        else:
            self.__value = None

    # -------------------------------------------------------------------------------------------- #

    @property
    def hed(self):
        """
        Hierarchical Event Descriptor (HED) Tag.
        """
        return self.__hed

    @hed.setter
    def hed(self, hed):
        if hed:
            if isinstance(hed, str):
                self.__hed = hed
            else:
                raise HedError(hed)
        else:
            self.__hed = None

    # -------------------------------------------------------------------------------------------- #

    @property
    def stim_file(self):
        """
        Represents the location of the stimulus file (such as an image, video, or audio file)
        presented at the given onset time.
        """
        return self.__stim_file

    @stim_file.setter
    def stim_file(self, stim_file):
        if stim_file:
            if isinstance(stim_file, str):
                self.__stim_file = stim_file
            else:
                raise StimFileError(stim_file)
        else:
            self.__stim_file = None

    # -------------------------------------------------------------------------------------------- #

    @property
    def identifier(self):
        """
        Represents the database identifier of the stimulus file presented at the given onset time.
        """
        return self.__identifier

    @identifier.setter
    def identifier(self, identifier):
        if identifier:
            if isinstance(identifier, str):
                self.__identifier = identifier
            else:
                raise IdentifierError(identifier)
        else:
            self.__identifier = None

    # -------------------------------------------------------------------------------------------- #

    @property
    def database(self):
        """
        Represents the database of the stimulus file presented at the given onset time.
        """
        return self.__database

    @database.setter
    def database(self, database):
        if database:
            if isinstance(database, str):
                self.__database = database
            else:
                raise DatabaseError(database)
        else:
            self.__database = None


# ----------------------------------------------------------------------------------------------- #


class BIDSError(Exception):
    """Base class for all BIDS Exceptions"""


# ----------------------------------------------------------------------------------------------- #


class OnsetError(BIDSError):
    """
    Raised if onset is not correct

    Attributes
    ----------
    onset : object
        Input which caused the error
    msg : str
        Explanation of the error
    """

    def __init__(self, onset, msg="Property 'onset' MUST be a number"):
        self.onset = onset
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.onset} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class DurationError(BIDSError):
    """
    Raised if duration is not correct

    Attributes
    ----------
    duration : object
        Input which caused the error
    msg : str
        Explanation of the error
    """

    def __init__(
        self,
        duration,
        msg="Property 'duration' MUST be either zero or positive (or n/a if unavailable)",
    ):
        self.duration = duration
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.duration} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class TrialTypeError(BIDSError):
    """
    Raised if trial_type is not correct

    Attributes
    ----------
    trial_type : object
        Input which caused the error
    msg : str
        Explanation of the error
    """

    def __init__(self, trial_type, msg="Property 'trial_type' MUST be a string"):
        self.trial_type = trial_type
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.trial_type} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class SampleError(BIDSError):
    """
    Raised if sample is not correct

    Attributes
    ----------
    sample : object
        Input which caused the error
    msg : str
        Explanation of the error
    """

    def __init__(self, sample, msg="Property 'sample' MUST be an integer"):
        self.sample = sample
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.sample} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class ResponseTimeError(BIDSError):
    """
    Raised if response_time is not correct

    Attributes
    ----------
    response_time : object
        Input which caused the error
    msg : str
        Explanation of the error
    """

    def __init__(
        self,
        response_time,
        msg="Property 'response_time' MUST be a number (or n/a if unavailable)",
    ):
        self.response_time = response_time
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.response_time} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class HedError(BIDSError):
    """
    Raised if hed is not correct

    Attributes
    ----------
    hed : object
        Input which caused the error
    msg : str
        Explanation of the error
    """

    def __init__(self, hed, msg="Property 'hed' MUST be a string"):
        self.hed = hed
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.hed} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class StimFileError(BIDSError):
    """
    Raised if stim_file is not correct

    Attributes
    ----------
    stim_file : object
        Input which caused the error
    msg : str
        Explanation of the error
    """

    def __init__(self, stim_file, msg="Property 'stim_file' MUST be a string"):
        self.stim_file = stim_file
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.stim_file} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class IdentifierError(BIDSError):
    """
    Raised if identifier is not correct

    Attributes
    ----------
    identifier : object
        Input which caused the error
    msg : str
        Explanation of the error
    """

    def __init__(self, identifier, msg="Property 'identifier' MUST be a string"):
        self.identifier = identifier
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.identifier} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class DatabaseError(BIDSError):
    """
    Raised if database is not correct

    Attributes
    ----------
    database : object
        Input which caused the error
    msg : str
        Explanation of the error
    """

    def __init__(self, database, msg="Property 'database' MUST be a string"):
        self.database = database
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.database} -> {self.msg}"
