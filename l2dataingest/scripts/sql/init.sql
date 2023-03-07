DECLARE
    collection SODA_COLLECTION_T;
    metadata VARCHAR2(4000) := '{"contentColumn" : { "name" : "DATA" }, "lastModifiedColumn" : { "name" : "LAST_MODIFIED"}, "creationTimeColumn" : { "name" : "CREATED_ON"}, "versionColumn" : { "name" : "VERSION" }}';
    status number := 0;
BEGIN
    status := DBMS_SODA.drop_collection('F1SIM-LAPDATA');
    status := DBMS_SODA.drop_collection('F1SIM-SESSION');
    status := DBMS_SODA.drop_collection('F1SIM-TELEMETRY');
    status := DBMS_SODA.drop_collection('F1SIM-MOTION');
    collection := DBMS_SODA.create_collection('F1SIM-LAPDATA',metadata);
    collection := DBMS_SODA.create_collection('F1SIM-SESSION',metadata);
    collection := DBMS_SODA.create_collection('F1SIM-TELEMETRY',metadata);
    collection := DBMS_SODA.create_collection('F1SIM-MOTION',metadata);
END;
/

DROP TABLE "F1SIM-DEVICE" CASCADE;
/

CREATE TABLE "F1SIM-DEVICE" (
    "M_TIMESTAMP" TIMESTAMP,
    "M_GAMEHOST" VARCHAR2(128),
    "M_DEVICENAME" VARCHAR2(128)
);
/

CREATE UNIQUE INDEX "F1SIM-DEVICE_PK" ON "F1SIM-DEVICE" ("M_GAMEHOST", "M_DEVICENAME");
/

ALTER TABLE "F1SIM-DEVICE" ADD CONSTRAINT "F1SIM-DEVICE_PK" PRIMARY KEY ("M_GAMEHOST", "M_DEVICENAME") USING INDEX ENABLE;
/
