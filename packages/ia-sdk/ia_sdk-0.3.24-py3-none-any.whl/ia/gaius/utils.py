"""Utility functions for interacting with GAIuS"""
import warnings
import json
import os
from copy import deepcopy


def create_gdf(strings=None,
               vectors=None,
               emotives=None,
               metadata=None) -> dict:
    """Create GDF using supplied list of strings, vectors, emotives, and/or
    metadata

    Args:
        strings (list, optional): Used to provide symbols as string data
            to GAIuS. Defaults to None.
        vectors (list, optional): Used to input vector data to GAIuS.
            Defaults to None.
        emotives (dict, optional): Used to provide emotional data to GAIuS.
            Defaults to None.
        metadata (dict, optional): Used to provide miscellaneous data to GAIuS.
            Defaults to None.

    Returns:
        dict: A dictionary representing the GDF

    Example:
        .. code-block:: python

            from ia.gaius.utils import create_gdf
            gdf = create_gdf(strings=["hello"], emotives={"happy": 10.0})


    .. warning::
        If fields provided are not of the type expected, a warning will be
        raised, but the GDF will still be made with the improper format
    """
    gdf = {
        "vectors": [] if vectors is None else vectors,
        "strings": [] if strings is None else strings,
        "emotives": {} if emotives is None else emotives,
        "metadata": {} if metadata is None else metadata
    }

    if not isinstance(gdf['vectors'], list):
        warnings.warn(UserWarning(f"vectors field is of type \
                                  {type(gdf['vectors'])}, expected list"))
    if not isinstance(gdf['strings'], list):
        warnings.warn(UserWarning(f"strings field is of type \
                                  {type(gdf['strings'])}, expected list"))
    if not isinstance(gdf['emotives'], dict):
        warnings.warn(UserWarning(f"emotives field is of type \
                                  {type(gdf['emotives'])}, expected dict"))
    if not isinstance(gdf['metadata'], dict):
        warnings.warn(UserWarning(f"metadata field is of type \
                                  {type(gdf['metadata'])}, expected dict"))

    return gdf


def log_progress(sequence, every=None, size=None, name='Items'):
    """
    A nice little Jupyter progress bar widget from:
    https://github.com/alexanderkuk/log-progress
    """
    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = int(size / 200)     # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    label.value = '{name}: {index} / ?'.format(
                        name=name,
                        index=index
                    )
                else:
                    progress.value = index
                    label.value = u'{name}: {index} / {size}'.format(
                        name=name,
                        index=index,
                        size=size
                    )
            yield record
    except Exception as e:
        print(f'Error in log_progress function: {str(e)})')
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = "{name}: {index}".format(
            name=name,
            index=str(index or '?')
        )


def abstract_names(ensemble: list) -> list:
    """Get a set of model names from a prediction ensemble

    Args:
        ensemble (list): a prediction ensemble

    Returns:
        list: list of models from predictions in the prediction ensemble

    Example:

        .. code-block:: python

            from ia.gaius.agent_client import AgentClient
            from ia.gaius.utils import abstract_names
            ...
            agent = AgentClient(agent_info)
            agent.connect()
            ...
            ensemble = agent.get_predictions(nodes=['P1'])
            models = abstract_names(ensemble)

    """
    return list(set([pred['name'] for pred in ensemble]))


def write_gdf_to_file(directory_name: str,
                      filename: str,
                      sequence: list) -> str:
    """Write a GDF sequence to a file

    Args:
        directory_name (str, required): directory to save GDFs to
        filename (str, required): filename to save to
        sequence (list, required): list of individual GDF events
            making up a sequence

    Example:
        .. code-block:: python

            from ia.gaius.utils import write_gdf_to_file, create_gdf
            sequence = [create_gdf(strings=["hello"]),
                        create_gdf(strings=["world"])]
            filename = 'hello_world'
            directory_name = '/example/dir'
            write_gdf_to_file(directory_name, filename, sequence)

    .. warning::
        Will overwrite the file at ``<directory_name>/<filename>``.
        Please ensure it is acceptable to do so.
        No safety checks are performed in this function

    """
    gdf_file_path = os.path.join(directory_name, filename)
    with open(gdf_file_path, 'w') as f:
        for event_idx, event in enumerate(sequence):
            json.dump(event, f)
            if event_idx != len(sequence) - 1:
                f.write('\n')

    return 'success'


def retrieve_bottom_level_records(traceback: dict) -> list:
    """Retrieve all records from a traceback
    (:func:`ia.gaius.agent_client.AgentClient.investigate_record`)
    call that have bottomLevel=True

    Args:
        traceback (dict): the dictionary pertaining to the output
            of an investigate call

    Returns:
        list: list of records from the traceback

    Example:
        .. code-block:: python

            from ia.gaius.agent_client import AgentClient
            from ia.gaius.utils import retrieve_bottom_level_records
            ...
            agent = AgentClient(agent_info)
            ...
            traceback_output = agent.investigate_record(record=record,
                                                        node=['P1'])
            bottom_level = retrieve_bottom_level_records(traceback_output)

    """
    bottom_level_records = []
    if traceback['bottomLevel'] is not True:
        for item_list in traceback['subitems']:
            for item in item_list:
                if isinstance(item, dict):
                    bottom_level_records.extend(retrieve_bottom_level_records(deepcopy(item)))
    else:
        bottom_level_records.append(traceback)

    return bottom_level_records
