"""dnres package is suitable for managing and sharing data and results from data analysis."""

import configparser
import contextlib
from datetime import datetime
import json
import os
import pickle
import platform
from rich import box
from rich.console import Console
from rich.table import Table
import sqlite3
import sys
from typing import Optional, Any
import warnings

class DnRes:
    """
    This class requires the path of a configuration "**.ini**" file for instantiation. 
    Upon instantiation, it checks if configuration file has errors, if structure path exists and if database path exists.
    """


    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.structure = None
        self.db = None
        self.description = None

        if not os.path.exists(self.config_file):
            raise FileNotFoundError('Config file does not exist.')

        self._check_config_for_errors()
        self._parse_config()

        # After parsing the config, the paths for structure and database should exist if they were provided.
        # If they don't exist, then it is assumed that it is a new analysis.

        if not os.path.exists(self.structure):
            print('Path "structure" in PATHS does not exist.')
            print('Create path "structure"?')
            while True:
                answer = input('[y/n]> ')
                if answer == 'y' or answer == 'n':
                    break
            if answer == 'y':
                os.makedirs(self.structure)
            else:
                exit("Action cancelled.")

        if not os.path.exists(self.db):
            print('Path "database" in PATHS does not exist.')
            print('Create path "database" and initialize database?')
            while True:
                answer = input('[y/n]> ')
                if answer == 'y' or answer == 'n':
                    break
            if answer == 'y':
                if not os.path.exists(os.path.dirname(self.db)):
                    os.makedirs(os.path.dirname(self.db))
                self._initialize_db()
            else:
                exit("Action cancelled.")

        self.console = Console()


    def _check_config_for_errors(self) -> None:
        """
        Expects the config file to have the sections "PATHS" and "INFO".
        It raises exception if they are missing.

        The "PATHS" section must include the keys "structure" and "database".
        In LINUX systems the paths may include "~".
        It raises exception if "PATHS" is empty and if the keys "structure" and "database" do not exist.

        The "INFO" section must have the key "description". It may have other keys, but it is optional.
        If "INFO" is empty or if "description" is missing then an exception is raised.
        """
        config = configparser.ConfigParser()
        config.read(self.config_file)
        if not config.has_section("PATHS"):
            raise KeyError("PATHS section is missing in configuration file.")

        if not config['PATHS']:
            raise KeyError("PATHS section in configuration file is empty.")

        if not config.has_section("INFO"):
            raise KeyError("INFO section is missing in configuration file.")

        if not config['INFO']:
            raise KeyError("INFO section in configuration file is empty.")

        if not config['PATHS'].get("structure", False):
            raise KeyError('The key "structure" is missing in PATHS section.')

        if not config['PATHS'].get("database", False):
            raise KeyError('The key "database" is missing in PATHS section.')

        if not config['INFO'].get("description", False):
            raise KeyError('The key "description" is missing in INFO section.')


    def _parse_config(self) -> None:
        """
        Parse config file and set self.structure, self.db and self.description.
        """
        config = configparser.ConfigParser()
        config.read(self.config_file)

        self.structure = config['PATHS']['structure']
        if platform.system() == "Linux" and self.structure.startswith('~/'):
            self.structure = os.path.expanduser(self.structure)

        self.db = config['PATHS']['database']
        if platform.system() == "Linux" and self.db.startswith('~/'):
            self.db = os.path.expanduser(self.db)

        self.description = config['INFO']['description']


    def _initialize_db(self) -> None:
        """Creates database based on the path specified in key database of the section PATHS."""
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                CREATE TABLE data(
                date INTEGER,
                path TEXT,
                datatype TEXT,
                description TEXT,
                source TEXT
                )
                """
                c.execute(query)
                conn.commit()

                query = """
                CREATE TABLE tags(
                tag TEXT,
                path TEXT
                )
                """
                c.execute(query)
                conn.commit()


    def _path_exists_in_db(self, path: str) -> bool:
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                SELECT 1 FROM data
                WHERE path=(?)
                """
                c.execute(query, (path, ))
                result = c.fetchone()
        if result:
            return True
        else:
            return False


    def _path_has_tag(self, path: str, tag: str) -> bool:
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                SELECT 1 FROM tags
                WHERE path=(?) AND tag=(?)
                """
                c.execute(query, (path, tag))
                result = c.fetchone()
        if result:
            return True
        else:
            return False


    def _register_path_in_db(self, 
                      date: int,
                      path: str,
                      datatype: str,
                      description: Optional[str],
                      source: Optional[str]) -> None:
        """Inserts path in database, or updates database if path already exists."""
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                if self._path_exists_in_db(path):
                    query = """
                    UPDATE data
                    SET date=(?),
                        datatype=(?),
                        description=(?),
                        source=(?)
                    WHERE path=(?)
                    """
                else:
                    query = """
                    INSERT INTO data 
                    (date, datatype, description, source, path) 
                    VALUES (?,?,?,?,?)
                    """
                c.execute(query, (date,
                                  datatype,
                                  description,
                                  source,
                                  path))
                conn.commit()


    def _register_tag_in_db(self, tag: str, path: str) -> None:
        """Inserts tagged path in database."""
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                INSERT INTO tags 
                (tag, path) 
                VALUES (?,?)
                """
                c.execute(query, (tag, path))
                conn.commit()


    def store(self, 
            data: Any, 
            tag: str,
            path: str, 
            description: Optional[str]=None,
            source: Optional[str]=None):
        """
        Stores specified data. Data is an object. Objects are serialized. Use this method if you want to store lists, dataframes and other similar objects. Note that previously stored data with the same path can be overwritten without warning.

        Parameters
        ----------
        data : any
            Data object to store. It could be any kind of object.
        tag : str
            Tag of stored data.
        path : str
            The path to store data. It should include the filename and have extension json or pickle.
        description : str, optional
            Defaults to None. Short description about the data.
        source : str, optional
            Defaults to None. Source of generated data. If None, the name of the calling script will be considered.
        """

        date = int(datetime.today().strftime('%Y%m%d'))
        serialization_methods = ["json", "pickle"]

        _, serialization = os.path.splitext(path)
        serialization = serialization.replace(".", '')

        if serialization not in serialization_methods:
            raise KeyError(f'Unknown serialization method "{serialization}". Valid methods: {serialization_methods}') 

        storePath = os.path.join(self.structure, path)
        storeDir = os.path.dirname(storePath)
        if not os.path.exists(storeDir):
            raise FileNotFoundError(f'Storing directory "{storeDir}" does not exist.')

        if serialization == 'json':
            with open(storePath, 'w') as outf:
                json.dump(data, outf)
        elif serialization == 'pickle':
            with open(storePath, 'wb') as outf:
                pickle.dump(data, outf)

        # Avoid duplicate entries from previously stored data with the same path and tag.
        if not self._path_exists_in_db(path):
            datatype = str(type(data))
            self._register_path_in_db(date, path, datatype, description, source)
        if not self._path_has_tag(path, tag):
            self._register_tag_in_db(tag, path)

        print('Data stored.')

    
    def tag(self, tag: str, path: str) -> None:
        """
        Add tag for given path.

        Parameters
        ----------
        tag : str
            Tag to add for path. 
        path : str
            Path to be tagged.
        """
        if not self._path_has_tag(path, tag):
            self._register_tag_in_db(tag, path)


    def set_info(self, 
            path: str, 
            datatype: Optional[str]=None,
            description: Optional[str]=None,
            source: Optional[str]=None):
        """
        Add or update info for path if info is not none.

        Parameters
        ----------
        path : str
            Path to update or add info.
        datatype : str, optional 
            Defaults to None. Datatype of path. Must be provided if path does not exist in database.
        description : str, optional 
            Defaults to None. Description of path. Must be provided if path does not exist in database.
        source : str, optional 
            Defaults to None. Source of path. Must be provided if path does not exist in database.
        """

        if self._path_exists_in_db(path):
            with contextlib.closing(sqlite3.connect(self.db)) as conn:
                with contextlib.closing(conn.cursor()) as c:
                    for col, value in zip(['datatype', 'description', 'source'], [datatype, description, source]):
                        if value:
                            query = f"""
                            UPDATE data 
                            SET {col}=(?) 
                            WHERE path=(?)
                            """
                            c.execute(query, (value, path))
                            conn.commit()
        else:
            if not datatype or not description or not source:
                raise KeyError(f'Path does not exist in database. You must provide datatype, description and source.') 
            date = int(datetime.today().strftime('%Y%m%d'))
            self._register_path_in_db(date, path, datatype, description, source)


    def load(self, path: str) -> Any:
        """
        Loads data from specified stored path. If path is not serialized object, it returns the path.

        Parameters
        ----------
        path : str
            The path of the stored data.

        Returns
        -------
        Python object, if path has the extension json or pickle. Otherwise, it returns the path.
        """

        storePath = os.path.join(self.structure, path)

        if not self._path_exists_in_db(path):
            raise FileNotFoundError('Path not found in database.')

        is_serialized = False
        if path.endswith('.json') or path.endswith('.pickle'):
            is_serialized = True

        if is_serialized:
            if not os.path.exists(storePath):
                raise FileNotFoundError('Path not found in structure.')
            if storePath.endswith('.json'):
                with open(storePath, 'r') as inf:
                    return json.load(inf)
            else:
                # data assumed to be pickled
                with open(storePath, 'rb') as inf:
                    return pickle.load(inf)
        else:
            return storePath


    def remove_from_db(self, path: str) -> None:
        """
        Removes path from database but not from structure.

        Parameters
        ----------
        path : str
            The path to remove from database.
        """
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                DELETE FROM data 
                WHERE path=(?)
                """
                c.execute(query, (path, ))
                conn.commit()

                query = """
                DELETE FROM tags 
                WHERE path=(?)
                """
                c.execute(query, (path, ))
                conn.commit()
        print("Done")


    def remove_tag(self, tag: str, path: str) -> None:
        """
        Removes given tag from given path in database.

        Parameters
        ----------
        tag : str
            The tag to remove from path.
        path : str
            The path to remove tag from.
        """
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                DELETE FROM tags
                WHERE path=(?) AND tag=(?)
                """
                c.execute(query, (path, tag))
                conn.commit()
        print("Done")


    def info(self, path: str) -> None:
        """
        Shows information for given path.

        Parameters
        ----------
        path : str
            Directory to show information.
        """

        if not self._path_exists_in_db(path):
            raise FileNotFoundError('Path not found in database.')

        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                cols = ['date', 'datatype', 'description', 'source']
                query = """
                SELECT {} FROM data 
                WHERE path=(?)
                """.format(','.join(cols))
                c.execute(query, (path, ))
                result = c.fetchone()

                query = """
                SELECT tag FROM tags 
                WHERE path=(?)
                """
                c.execute(query, (path, ))
                tags = c.fetchall()
        tags = [t[0] for t in tags]

        print("path: {}".format(os.path.join(self.structure, path)))
        for col,value in zip(cols, result): 
            print(f"{col}: {value}")
        print("tags: {}".format(', '.join(tags)))


    def _print_table(self, rows: list) -> None:
        """Prints rich table of given rows. Rows are list of lists or list of tuples."""
        table = Table(box=box.SIMPLE_HEAVY)
        table.add_column("Date", justify="left", no_wrap=True)
        table.add_column("Path", justify="left", no_wrap=True)
        table.add_column("Datatype", justify="left", no_wrap=True)
        table.add_column("Description", justify="left", no_wrap=False)
        table.add_column("Source", justify="left", no_wrap=False)
        for row in rows:
            # Make sure only strings are passed to table
            table.add_row(*list(map(str, row)))
        self.console.print(table)


    def __repr__(self):
        if not self.description:
            self.console.print("[bold magenta]Description[/bold magenta]: Not available")
        else:
            self.console.print(f"[bold magenta]Description[/bold magenta]: {self.description}")
        print()

        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = "SELECT DISTINCT(tag) FROM tags"
                c.execute(query)
                tags = c.fetchall()
        if tags:
            tags = [t[0] for t in tags]
            tags.sort()

            tagsRows = dict()
            cols = ['date', 'path', 'datatype', 'description', 'source']
            with contextlib.closing(sqlite3.connect(self.db)) as conn:
                with contextlib.closing(conn.cursor()) as c:
                    for tag in tags:
                        tagsRows[tag] = list()
                        query = "SELECT path FROM tags WHERE tag=(?)"
                        c.execute(query, (tag, ))
                        paths = c.fetchall()
                        paths = [p[0] for p in paths]
                        for path in paths:
                            query = "SELECT {} FROM data WHERE path=(?)".format(",".join(cols))
                            c.execute(query, (path, ))
                            results = c.fetchone()
                            if not results:
                                results = ("NA",path,"NA","NA","NA")
                            tagsRows[tag].append(results)

            for tag in tags:
                self.console.print(f"[bold magenta]{tag}[/bold magenta]")
                self._print_table(tagsRows[tag])
                print()
            return ''
        else:
            return "No entries found."


