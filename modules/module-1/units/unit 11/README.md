# 📁 SQL Schema and Data – COMPANY1

## 📦 Schema and Tables

```sql
CREATE SCHEMA `company1` DEFAULT CHARACTER SET utf8;
```

### 🧾 Table: `emp`

```sql
CREATE TABLE `company1`.`emp` (
  `EMPNO` INT NOT NULL AUTO_INCREMENT,
  `ENAME` VARCHAR(155) NULL,
  `JOB` VARCHAR(155) NULL,
  `MGR` INT NULL,
  `HIREDATE` DATE NULL,
  `SAL` DECIMAL(10,2) NULL DEFAULT 0.00,
  `COMM` DECIMAL(10,2) NULL DEFAULT 0.00,
  `DEPTNO` INT NULL,
  PRIMARY KEY (`EMPNO`)
);
```

### 🔍 Indexes in table `emp`
Add composite index on both the manager and the employee.
Add composite index on both the department and the employee.
Add index on department
Add index on manager

```sql
ALTER TABLE `company1`.`emp`
ADD INDEX `idxMGR` (`MGR` ASC),
ADD INDEX `idxDEP` (`DEPNO` ASC),
ADD INDEX `idxMGREmp` (`MGR` ASC, `EMPNO` ASC),
ADD INDEX `idxDEPEmp` (`DEPTNO` ASC, `EMPNO` ASC);
```

### 🧾 Table: `dept`

```sql
CREATE TABLE `company1`.`dept` (
  `DEPTNO` INT NOT NULL AUTO_INCREMENT,
  `DNAME` VARCHAR(155) NULL,
  `LOC` VARCHAR(155) NULL,
  PRIMARY KEY (`DEPTNO`)
);
```

### 🔗 Foreign Key Constraint
Only allow records where DEPTNO exists in table `dept` by 'linking' to the primary key of the table `dept`.
This is also often called LOOKUP.
This ensure data integrity. When a record in `dept` is remove the associating records in emp will be set to NULL.

```sql
ALTER TABLE `company1`.`emp` 
ADD CONSTRAINT `depNumber`
  FOREIGN KEY (`DEPTNO`)
  REFERENCES `company1`.`dept` (`DEPTNO`)
  ON DELETE SET NULL
  ON UPDATE NO ACTION;
```
---

## 📥 Data Insert Statements

### 🔹 Departments

```sql
INSERT INTO dept (DEPTNO, DNAME, LOC) VALUES
(10, 'ACCOUNTING', 'NEW YORK'),
(20, 'RESEARCH', 'DALLAS'),
(30, 'SALES', 'CHICAGO');
```

### 🔹 Employees

```sql
INSERT INTO emp (EMPNO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPTNO) VALUES
(7369, 'SMITH', 'CLERK', 7902, '1980-12-17', 800, NULL, 20),
(7499, 'ALLEN', 'SALESMAN', 7698, '1981-02-20', 1600, 300, 30),
(7521, 'WARD', 'SALESMAN', 7698, '1981-02-22', 1250, 500, 30),
(7566, 'JONES', 'MANAGER', 7839, '1981-04-02', 2975, NULL, 20),
(7654, 'MARTIN', 'SALESMAN', 7698, '1981-09-28', 1250, 1400, 30),
(7698, 'BLAKE', 'MANAGER', 7839, '1981-05-01', 2850, NULL, 30),
(7782, 'CLARK', 'MANAGER', 7839, '1981-06-09', 2450, NULL, 10),
(7788, 'SCOTT', 'ANALYST', 7566, '1987-04-19', 3000, NULL, 20),
(7839, 'KING', 'PRESIDENT', NULL, '1981-11-17', 5000, NULL, 10),
(7844, 'TURNER', 'SALESMAN', 7698, '1981-09-08', 1500, 0, 30),
(7876, 'ADAMS', 'CLERK', 7788, '1987-05-23', 1100, NULL, 20),
(7900, 'JAMES', 'CLERK', 7698, '1981-12-03', 950, NULL, 30),
(7902, 'FORD', 'ANALYST', 7566, '1981-12-03', 3000, NULL, 20),
(7934, 'MILLER', 'CLERK', 7782, '1982-01-23', 1300, NULL, 10);
```
---

# 📊 SQL Programming Exercise

## ✅ Tasks

### 1. List all Employees whose salary is greater than 1,000 but not 2,000.
**Show:** Employee Name, Department, Salary  
**(4 marks)**
- Could also be solved by using BETWEEN. I however do like to not be database depended (locked).
```sql
SELECT a.ENAME, b.DNAME, a.SAL
FROM emp a
INNER JOIN dept b ON a.DEPTNO = b.DEPTNO
WHERE (a.SAL >= 1000 AND a.SAL < 2000);
```

---

### 2. Count the number of people in department 30 who receive a salary and a commission.
**(4 marks)**

```sql
SELECT COUNT(a.EMPNO)
FROM emp a
INNER JOIN dept b ON a.DEPTNO = b.DEPTNO
WHERE (b.DEPTNO = 30 AND a.SAL > 0 AND a.COMM > 0);
```
Alternative (only use 1 table) == faster:
```sql
SELECT COUNT(a.EMPNO)
FROM emp a
WHERE (a.DEPTNO = 30 AND a.SAL > 0 AND a.COMM > 0);
```
---

### 3. Find the name and salary of the employees that have a salary ≥ 1000 and live in Dallas.
**(4 marks)**

```sql
SELECT a.ENAME, a.SAL
FROM emp a
INNER JOIN dept b ON a.DEPTNO = b.DEPTNO
WHERE (b.LOC = 'DALLAS' AND a.SAL >= 1000);
```

Alternative using subquery
```sql
SELECT a.ENAME, a.SAL
FROM emp a
INNER JOIN (
    SELECT DEPTNO
    FROM dept
    WHERE LOC='DALLAS'
)b ON a.DEPTNO=b.DEPTNO
WHERE a.SAL >= 1000;
```
---

### 4. Find all departments that do not have any current employees.
**(4 marks)**

```sql
SELECT a.DEPTNO
FROM dept a
WHERE a.DEPTNO NOT IN (
  SELECT b.DEPTNO
  FROM emp b
);
```
Alternative (static)
```sql
SELECT b.DEPTNO
FROM emp b
WHERE b.DEPTNO NOT IN (10,20,30);
```

---

### 5. List the department number, the average salary, and the count of employees per department.
**(4 marks)**

```sql
SELECT a.DEPTNO, AVG(a.SAL) AS AVGSAL, COUNT(a.EMPNO) AS NOEMPL
FROM emp a
GROUP BY a.DEPTNO;
```