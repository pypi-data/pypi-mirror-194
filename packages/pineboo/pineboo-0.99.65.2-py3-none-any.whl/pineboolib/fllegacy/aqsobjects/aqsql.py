# -*- coding: utf-8 -*-
"""
AQSql Module.

Provide queries to DB.
"""
from enum import IntEnum, unique, Enum

from pineboolib import application, logging
from pineboolib.application import types
from pineboolib.application.database import pnsqlcursor

from typing import Union, Any, List, TYPE_CHECKING


if TYPE_CHECKING:
    from pineboolib.interfaces import iconnection, isqlcursor  # pragma: no cover

LOGGER = logging.get_logger(__name__)


class TableType(Enum):
    """TableType class."""

    Tables: int = 1  # pylint: disable=invalid-name
    SystemTables: int = 2  # pylint: disable=invalid-name
    Views: int = 3  # pylint: disable=invalid-name
    AllTables: int = 0  # pylint: disable=invalid-name


class AQSql(object):
    """AQSql Class."""

    Insert: int = 0
    Edit: int = 1
    Del: int = 2
    Browse: int = 3

    @unique
    class TableType(IntEnum):
        """TableType class."""

        Tables = 0x01  # pylint: disable=invalid-name
        SystemTables = 0x02  # pylint: disable=invalid-name
        Views = 0x04  # pylint: disable=invalid-name
        AllTables = 0xFF  # pylint: disable=invalid-name

    @classmethod
    def database(self, connection_name: str = "default") -> "iconnection.IConnection":
        """Return the database of a connection."""

        if application.PROJECT.conn_manager is None:
            raise Exception("Project is not connected yet")
        return application.PROJECT.conn_manager.useConn(connection_name)

    @classmethod
    def update(
        self,
        table_or_cursor: Union[str, "isqlcursor.ISqlCursor"],
        fields: Union[List[str], types.Array],
        values: Union[List[Any], types.Array],
        where: str = "",
        conn: str = "default",
    ):
        """Update a set of cursor records with new values."""
        cur: "isqlcursor.ISqlCursor"

        if isinstance(table_or_cursor, str):
            cur = pnsqlcursor.PNSqlCursor(table_or_cursor, conn)
        else:
            cur = table_or_cursor

        # if cur is None:
        #     return False

        if not cur.metadata():
            return False

        cur.select(where)

        ret_ = True
        activate_check_integrity = cur.activatedCheckIntegrity()

        fields_count = len(fields)

        while ret_ and cur.next():
            cur.setModeAccess(cur.Edit)
            cur.refreshBuffer()

            for i in range(0, fields_count - 1):
                cur.setValueBuffer(fields[i], values[i])

            msg_check_integrity = cur.msgCheckIntegrity()
            if msg_check_integrity != "":
                raise Exception(msg_check_integrity)

            cur.setActivatedCheckIntegrity(False)
            ret_ = cur.commitBuffer()
            cur.setActivatedCheckIntegrity(activate_check_integrity)

        return ret_

    @classmethod
    def insert(
        self,
        table_or_cursor: Union[str, "isqlcursor.ISqlCursor"],
        fields: Union[List[str], types.Array],
        values: Union[List[Any], types.Array],
        where: str = "",
        conn: str = "default",
    ):
        """Insert a record in a cursor."""
        cur: "isqlcursor.ISqlCursor"

        if isinstance(table_or_cursor, str):
            cur = pnsqlcursor.PNSqlCursor(table_or_cursor, conn)
        else:
            cur = table_or_cursor

        if not cur.metadata():
            return False

        fields_count = len(fields)

        cur.setModeAccess(cur.Insert)
        cur.refreshBuffer()

        for i in range(fields_count):
            cur.setValueBuffer(fields[i], values[i])

        msg_check_integrity = cur.msgCheckIntegrity()
        if msg_check_integrity != "":
            raise Exception(msg_check_integrity)

        ret_ = False
        activated_check_integrity = cur.activatedCheckIntegrity()
        cur.setActivatedCheckIntegrity(False)
        ret_ = cur.commitBuffer()
        cur.setActivatedCheckIntegrity(activated_check_integrity)

        return ret_

    @classmethod
    def del_(
        self,
        cur_or_table: Union[str, "isqlcursor.ISqlCursor"],
        where: str = "",
        conn_name: str = "default",
    ):
        """Remove a recordset from a cursor."""

        cur: "isqlcursor.ISqlCursor"

        if not isinstance(cur_or_table, str):
            cur = cur_or_table
        else:
            cur = pnsqlcursor.PNSqlCursor(cur_or_table, True, conn_name)

        act_check = cur.activatedCheckIntegrity()

        cur.select(where)
        if cur.first():
            while True:
                cur.setModeAccess(cur.Del)
                cur.refreshBuffer()
                cur.setActivatedCheckIntegrity(False)
                res_commit = cur.commitBuffer()
                cur.setActivatedCheckIntegrity(act_check)
                if not res_commit:
                    return False

                if not cur.next():
                    break

        return True


"""
FIXME!!: crear todos los emun...
Código C++ original
class AQSql : public QObject
{
  Q_OBJECT

  Q_ENUMS(ModeAccess)
  Q_ENUMS(ConnOptions)
  Q_ENUMS(SpecialType)
  Q_ENUMS(Cardinality)
  Q_ENUMS(TableType)
  Q_ENUMS(SqlErrorType)
  Q_ENUMS(Refresh)

public:
  enum ModeAccess {
    Insert = 0,
    Edit = 1,
    Del = 2,
    Browse = 3
  };

  enum ConnOptions {
    User = 0,
    Password = 1,
    Port = 2,
    Host = 3
  };

  enum SpecialType {
    Serial = 100,
    Unlock = 200,
    Check = 300
  };

  enum Cardinality {
    RELATION_1M = 0,
    RELATION_M1 = 1
  };

  enum SqlErrorType {
    SqlErrorNone,
    SqlErrorConnection,
    SqlErrorStatement,
    SqlErrorTransaction,
    SqlErrorUnknown
  };

  enum Refresh {
    RefreshData = 1,
    RefreshColumns = 2,
    RefreshAll = 3
  };

  AQSql() : QObject(0, "aqs_aqsql") {}

  void throwError(const QString &msg, FLSqlDatabase *db) {
    if (!db->qsaExceptions() || !globalAQSInterpreter) {
      qWarning(msg);
      return;
    }
    if (globalAQSInterpreter->isRunning())
      globalAQSInterpreter->throwError(msg);
    else
      qWarning(msg);
  }

public slots:
  /**
  Añade una base de datos a las conexiones disponibles.

  La base de datos será abierta. Si ya existiera una conexión con el mismo nombre
  la base datos correspondiente será cerrada y borrada, sustituyéndola por la nueva.

  @param driverAlias Alias del driver ( PostgreSQL, MySQL, SQLite, ... ), ver FLSqlDatabase.
  @param nameDB  Nombre de la base de datos a la que conectar
  @param user  Usuario de la conexión
  @param password Contraseña para el usuario
  @param host  Nombre o dirección del servidor de la base de datos
  @param port  Puerto TCP de conexion
  @param connectionName Nombre de la conexion
    @param connectOptions Contiene opciones auxiliares de conexión a la base de datos.
                        El formato de la cadena de opciones es una lista separada por punto y coma
                        de nombres de opción o la opción = valor. Las opciones dependen del uso del
                        driver de base de datos.
  @return TRUE si se pudo realizar la conexión, FALSE en caso contrario
  */
  bool addDatabase(const QString &driverAlias, const QString &nameDB, const QString &user,
                   const QString &password, const QString &host, int port,
                   const QString &connectionName, const QString &connectOptions = QString::null) {
    return FLSqlConnections::addDatabase(driverAlias, nameDB, user, password, host, port,
                                         connectionName, connectOptions);
  }

  /**
  Sobrecargada por conveniencia

  Practicamente hace lo mismo que el método anterior pero utilizando una base de datos ya construida

  @param db  Base datos a añadir a las conexiones disponibles, ver FLSqlDatabase.
  @param connectionName Nombre de la conexion
  @return TRUE si se pudo realizar la conexión, FALSE en caso contrario
  */
  bool addDatabase(FLSqlDatabase *db, const QString &connectionName = "default") {
    return FLSqlConnections::addDatabase(db, connectionName);
  }

  /**
  Sobrecargada por conveniencia

  Añade una base de datos a las conexiones disponibles utilizando los datos de otra conexión

  @param newConnName    Nombre a utilizar para la nueva conexion
  @param sourceConnName Nombre de una conexión existente a utilizar como origen de los datos de conexión
  @return TRUE si se pudo realizar la conexión, FALSE en caso contrario
  */
  bool addDatabase(const QString &newConnName, const QString &sourceConnName = "default") {
    FLSqlDatabase *srcDb = FLSqlConnections::database(sourceConnName);
    if (!srcDb)
      return false;
    return FLSqlConnections::addDatabase(srcDb->driverName(), srcDb->database(),
                                         srcDb->user(), srcDb->password(), srcDb->host(),
                                         srcDb->port(), newConnName);
  }

  /**
  Elimina una base de datos de las conexiones disponibles.

  Cierra la base de datos correspondiente y la elimina.

  @param connectionName Nombre de la conexion
  @return TRUE si se pudo eliminar la base de datos, FALSE en caso contrario
  */
  bool removeDatabase(const QString &connectionName) {
    return FLSqlConnections::removeDatabase(connectionName);
  }

  /**
  Obtiene la base de datos de una conexion.

  @param connectionNmae Nombre de la conexion
  @return La base de datos correspondiente al nombre de conexion indicado
  */
  FLSqlDatabase *database(const QString &connectionName = "default") {
    return FLSqlConnections::database(connectionName);
  }

  /**
  Finalizar todas las conexiones
  */
  void finish() {
    FLSqlConnections::finish();
  }

  /**
  Inserta un registro en un cursor

  Si hay un error SQL, eleva una excepción con el mensaje de error

  Ejemplo:

  var cur = new AQSqlCursor("clientes");
  try {
    AQSql.insert(cur,
                 ["codcliente","nombre","cifnif","codserie"],
                 ["1","pepe","XYZ","A"]);
  } catch (e) {
    sys.errorMsgBox("Error SQL: " + e);
  }
  */
  bool insert(FLSqlCursor *cur, const QStringList &fields,
              const QValueList<QVariant> &values) {
    if (!cur)
      return false;

    if (!cur->metadata()) {
      throwError(
        tr("No hay metadatos para '%1'").arg(cur->QObject::name()), cur->db()
      );
      return false;
    }

    int fields_count = fields.size();
    int valuesCount = values.size();

    cur->setModeAccess(Insert);
    if (!cur->refreshBuffer())
      return false;
    for (int i = 0; i < fields_count; ++i)
      cur->setValueBuffer(fields[i], (i < valuesCount ? values[i] : QVariant()));

    QString msgCheck(cur->msgCheckIntegrity());
    if (!msgCheck.isEmpty()) {
      throwError(msgCheck, cur->db());
      return false;
    }

    bool actCheck = cur->activatedCheckIntegrity();
    cur->setActivatedCheckIntegrity(false);
    bool ok = cur->commitBuffer();
    cur->setActivatedCheckIntegrity(actCheck);
    return ok;
  }

  bool insert(const QString &table, const QStringList &fields,
              const QValueList<QVariant> &values,
              const QString &connName = "default") {
    AQSqlCursor cur(table, true, connName);
    return insert(&cur, fields, values);
  }

  /**
  Actualiza un conjunto de registros de un cursor con nuevos valores

  Si hay un error SQL, eleva una excepción con el mensaje de error

  Ejemplo:

  var cur = new AQSqlCursor("clientes");
  try {
    AQSql.update(cur,
                 ["nombre","cifnif","codserie"],
                 ["juan","ZYX","A"],
                 "codcliente='1'");
  } catch (e) {
    sys.errorMsgBox("Error SQL: " + e);
  }
  */
  bool update(FLSqlCursor *cur, const QStringList &fields,
              const QValueList<QVariant> &values, const QString &where = "") {
    if (!cur)
      return false;

    if (!cur->metadata()) {
      throwError(
        tr("No hay metadatos para '%1'").arg(cur->QObject::name()), cur->db()
      );
      return false;
    }

    if (!cur->select(where))
      return false;

    bool ok = true;
    QString msgCheck;
    bool actCheck = cur->activatedCheckIntegrity();
    int fields_count = fields.size();
    int valuesCount = values.size();

    while (ok && cur->next()) {
      cur->setModeAccess(Edit);
      if (!cur->refreshBuffer()) {
        ok = false;
        break;
      }
      for (int i = 0; i < fields_count; ++i)
        cur->setValueBuffer(fields[i], (i < valuesCount ? values[i] : QVariant()));

      msgCheck = cur->msgCheckIntegrity();
      if (!msgCheck.isEmpty()) {
        ok = false;
        throwError(msgCheck, cur->db());
        break;
      }

      cur->setActivatedCheckIntegrity(false);
      ok = cur->commitBuffer();
      cur->setActivatedCheckIntegrity(actCheck);
    }
    return ok;
  }

  bool update(const QString &table, const QStringList &fields,
              const QValueList<QVariant> &values, const QString &where = "",
              const QString &connName = "default") {
    AQSqlCursor cur(table, true, connName);
    cur.setForwardOnly(true);
    return update(&cur, fields, values, where);
  }

  /**
  Elimina un conjunto de registros de un cursor

  Si hay un error SQL, eleva una excepción con el mensaje de error

  Ejemplo:

  var cur = new AQSqlCursor("clientes");
  try {
    AQSql.del(cur, "codcliente='1'");
  } catch (e) {
    sys.errorMsgBox("Error SQL: " + e);
  }
  */
  bool del(FLSqlCursor *cur, const QString &where = "") {
    if (!cur)
      return false;

    if (!cur->metadata()) {
      throwError(
        tr("No hay metadatos para '%1'").arg(cur->QObject::name()), cur->db()
      );
      return false;
    }

    if (!cur->select(where))
      return false;

    bool ok = true;
    QString msgCheck;
    bool actCheck = cur->activatedCheckIntegrity();

    while (ok && cur->next()) {
      cur->setModeAccess(Del);
      if (!cur->refreshBuffer()) {
        ok = false;
        break;
      }

      msgCheck = cur->msgCheckIntegrity();
      if (!msgCheck.isEmpty()) {
        ok = false;
        throwError(msgCheck, cur->db());
        break;
      }

      cur->setActivatedCheckIntegrity(false);
      ok = cur->commitBuffer();
      cur->setActivatedCheckIntegrity(actCheck);
    }
    return ok;
  }

  bool del(const QString &table, const QString &where = "",
           const QString &connName = "default") {
    AQSqlCursor cur(table, true, connName);
    cur.setForwardOnly(true);
    return del(&cur, where);
  }

  /**
  Ejecuta una consulta y devuelve información de la misma y el conjunto de
  registros obtenidos

  Si hay un error SQL, eleva una excepción con el mensaje de error

  Devuelve un array 'A' donde:

  -A[0] contiene el número de registros
  -A[1] contiene el número de campos
  -A[2] contiene otro array con los nombres de lo campos, en orden correlativo
        al que aparecen en la consulta
  -A[3..fin] los valores de los campos, en grupos de tamaño A[1]

  Ejemplo:

  var records;
  try {
    records = AQSql.select("bancos.*", "bancos");
    if (!records.length)
      return;

    var size = records[0];
    var nFields = records[1];
    var fieldNames = records[2];

    var rec = "";
    for (var i = 0; i < nFields; ++i)
      rec += fieldNames[i] + "    | ";
    print(rec);
    print("==============================================");

    for (var i = 3; i <= size * nFields;  i += nFields) {
      rec = "";
      for (var j = 0; j < nFields; ++j) {
        rec += records[i + j] + " | ";
      }
      print(rec);
    }
  } catch (e) {
    sys.errorMsgBox("Error SQL: " + e);
  }
  */
  QValueList<QVariant> select(const QString &select,
                              const QString &from,
                              const QString &where = QString::null,
                              const QString &orderBy = QString::null,
                              const QString &connName = "default") {
    AQSqlQuery qry(0, connName);
    qry.setTablesList(from);
    qry.setSelect(select);
    qry.setFrom(from);
    qry.setWhere(where);
    qry.setOrderBy(orderBy);
    qry.setForwardOnly(true);
    if (!qry.exec())
      return QVariantList();

    QVariantList ret;
    int countFields = qry.fieldList().count();

    ret.append(qry.size());
    ret.append(countFields);
    ret.append(qry.fieldList());

    while (qry.next()) {
      for (int i = 0; i < countFields; ++i)
        ret.append(qry.value(i));
    }

    return ret;
  }

  /**
  Esencialmente hace lo mismo que AQSql::select(), pero con la diferencia que reservará
  un bloqueo sobre los registros que devuelve la consulta.

  Si hay otro selectForUpdate anterior sobre los mismos o algunos registros que obtiene la
  consulta esta llamanda quedará en espera, bloqueada sobre esos registros, hasta que termine
  la transacción que inició el otro selectForUpdate.

  En PostgreSQL se puede utizar el parámetro 'nowait'. Si es TRUE y si al ejecutar la
  consulta se detecta que se va a caer en un bloqueo, es decir hay otro selectForUpdate anterior,
  no se bloqueará la llamada, y se elevará una excepción, terminando la transacción en curso.
  El parámetro 'nowait' no tiene efecto para cualquier otra base de datos distinta a PostgreSQL.
  */
  QValueList<QVariant> selectForUpdate(const QString &select,
                                       const QString &from,
                                       const QString &where = QString::null,
                                       bool nowait = false,
                                       const QString &connName = "default") {
    AQSqlQuery qry(0, connName);
    qry.setTablesList(from);
    qry.setSelect(select);
    qry.setFrom(from);
    QString w(where.isEmpty() ? "1=1" : w);
    qry.setWhere(nowait ?
                 w + QString::fromLatin1(" FOR UPDATE NOWAIT") :
                 w + QString::fromLatin1(" FOR UPDATE"));
    qry.setForwardOnly(true);
    if (!qry.exec())
      return QVariantList();

    QVariantList ret;
    int countFields = qry.fieldList().count();

    ret.append(qry.size());
    ret.append(countFields);
    ret.append(qry.fieldList());

    while (qry.next()) {
      for (int i = 0; i < countFields; ++i)
        ret.append(qry.value(i));
    }

    return ret;
  }
};
"""
