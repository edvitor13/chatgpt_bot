from __future__ import annotations
import sqlite3



class Database(sqlite3.Connection):
    
    """
    Gerencia conexão com banco de dados sqlite3.
    """
    
    def __init__(self, database:str=":memory:", **kwargs) -> None:
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
        - database: nome do arquivo do banco de dados. Usa ":memory:" se nenhum nome for passado.
        - kwargs: outros argumentos opcionais para a conexão.
        """
        super().__init__(database, **kwargs)
        
        # Modificando comportamento padrão do retorno de dados
        self.row_factory = Database._dict_factory
        
        self.cur: sqlite3.Cursor = None

        self._create_functions()


    def execute(self, *args, **kwargs) -> sqlite3.Cursor:
        """
        Executa um cursor.
        
        Args:
        - *args: argumentos para a execução do cursor.
        - **kwargs: argumentos opcionais para a execução do cursor.
        
        Returns:
        - O próprio cursor, após sua execução.
        """
        self.cur = self.cursor().execute(*args, **kwargs)
        return self.cur


    def commit_close(self) -> None:
        """
        Executa o commit e fecha a conexão.
        """
        self.commit()
        self.close()


    def _create_functions(self) -> Database:
        """
        Adiciona novas funcionalidades à conexão.
        
        Returns:
        - A própria conexão.
        """
        # nr == normal_replace
        self.create_function(
            "nr", 1, Database._function_normal_replace)

        return self


    @staticmethod
    def _function_normal_replace(arg:str) -> str:
        """
        Funcionalidade "nr"
        Substitui todos caracteres com acentuação e especiais 
        por sua versão base para facilitar nas buscas.
        
        Args:
        - arg: string a ser substituída.
        
        Returns:
        - A string com as substituições realizadas.
        """
        replace_list = [
            (["á", "à", "â", "ã"], "a"),
            (["ó", "ô", "õ"], "o"),
            (["é", "ê"], "e"),
            (["ú", "ü"], "u"),
            (["í"], "i"),
            (["ç"], "c"),
        ]

        for replacer, replace in replace_list:
            for char in replacer:
                arg = arg.replace(char, replace)
                arg = arg.replace(char.upper(), replace.upper())

        return arg


    @staticmethod
    def _dict_factory(cursor: sqlite3.Cursor, row: list) -> dict:
        """
        Funcionalidade Factory
        Para alterar comportamento padrão de retorno de dados de (v1, v2) para {k1 -> v, k2 -> v}.
        
        Args:
        - cursor: cursor que contém as informações das colunas.
        - row: lista com os valores das colunas.
        
        Returns:
        - Dicionário com os pares chave-valor correspondentes às colunas e valores da linha atual.
        """

        data = {}
        for idx, col in enumerate(cursor.description):
            data[col[0]] = row[idx]
        return data
