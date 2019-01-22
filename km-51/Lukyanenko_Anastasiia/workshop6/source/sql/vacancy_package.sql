CREATE OR REPLACE PACKAGE vacancy_package AS
    TYPE vacancy_row IS RECORD (
vacancy_name vacancy.vacancy_name%TYPE,
company vacancy.company%TYPE,
email vacancy.email%TYPE,
salary vacancy.salary%TYPE,
location vacancy.location%TYPE,
sphere vacancy.sphere%TYPE
);

TYPE vacancy_table IS
 TABLE OF vacancy_row;

FUNCTION get_vacancy (
p_vacancy_name   IN          vacancy.vacancy_name%TYPE,
p_email   IN          vacancy.email%TYPE
)
RETURN vacancy_table
        PIPELINED;


END vacancy_package;
/


CREATE OR REPLACE PACKAGE BODY vacancy_package AS

    FUNCTION get_vacancy (
        p_vacancy_name   IN          vacancy.vacancy_name%TYPE,
        p_email   IN          vacancy.email%TYPE
    ) RETURN vacancy_table
        PIPELINED
    IS
    BEGIN
        FOR curr IN (
            SELECT DISTINCT
                vacancy_name,
                company,
                email,
                salary,
                location,
                sphere
                FROM
                vacancy
            WHERE
                vacancy.vacancy_name = p_vacancy_name AND
                vacancy.email = p_email
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;
    END get_vacancy;

END vacancy_package;
/
