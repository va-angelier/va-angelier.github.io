# README – Interest Book in Python (Jupyter Notebook)

## 1. Introduction

This project is part of the Unit 10 submission for the Programming and Testing module. It extends the work completed in Part 1, where the initial logic and pseudocode were implemented in PHP. For Part 2, the application has been rewritten in Python and executed in a Jupyter Notebook, in line with academic requirements for algorithm development, testing and validation.

The transition from PHP to Python was made intentionally to demonstrate the underlying logic in a different language and to take advantage of Jupyter Notebook's interactive capabilities for testing and documentation. With over 25 years of programming experience, including extensive work in PHP and Python (see [linkedin.com/in/victorangelier](https://www.linkedin.com/in/victorangelier/)), I am comfortable working across languages and platforms. This assignment reflects both my academic progress and professional experience in data-driven development.

The goal remains the same: to build a personal digital repository for storing, organising, and retrieving online resources using structured data and well-tested logic. All development was done without external libraries, in accordance with the assignment constraints.

## 2. Application Description

The Interest Book allows users to:

- Add new resource records
- Search for resources using tags or keywords
- Delete existing records
- Edit records by URI
- Sort all records by creation date
- Interact via a simple, menu-driven interface

Each record contains:
- A **title** (string)
- A **URI** (string)
- Between **1 and 5 descriptive tags** (list of strings)
- A **created_at** timestamp
- An **accessed_at** timestamp

Records are stored in memory using a Python list of dictionaries, each representing a resource. The application uses only core Python features, in line with algorithmic and data structure principles from the module (Cormen et al., 2009).

## 3. Data Structure and Algorithm Design

The application's core data structure is a list of records (`records[]`), where each record is a Python dictionary:

```python
{
    "title": "Machine Learning Basics",
    "uri": "https://ml.org",
    "tags": ["ai", "ml"],
    "created_at": "2025-04-01T09:45:00",
    "accessed_at": "2025-04-01T09:45:00"
}
```

Key algorithms implemented include:

- **Bubble sort** for ordering by `created_at`
- **Linear search** for searching by tags, keyword, or URI
- **Validation** logic for tag limits and URI uniqueness
- **Update and deletion logic** with confirmation prompts

## 4. Interface Design

A menu loop is provided in the function `main_menu()`, which enables interaction via keyboard input. Each user action (add, search, delete, edit, sort) is accessible via a numbered menu, and users are prompted for input as required.

Before deleting or editing a record, users are asked for confirmation, aligning with the requirement to “get a prompt before an action is performed”.

## 5. Testing Strategy

Testing was based on the plan defined in Part 1 (Section 3), covering:

- **Normal cases (happy flow)** – e.g. adding valid records, retrieving known tags
- **Boundary tests** – e.g. exceeding the tag limit, searching for missing tags, deleting a non-existent record
- **Input validation** – e.g. empty fields, incorrect types

All tests were executed in Jupyter Notebook cells, each preceded by a markdown heading. Screenshots were taken of the output and are included with the submission.

## 6. How to Run

To run the Interest Book application:

1. Install Python 3 and Jupyter Notebook (via `pip install notebook`)
2. Launch Jupyter by running `jupyter notebook` in a terminal
3. Open the notebook file (e.g. `interest_book.ipynb`)
4. Run the code cells to initialise the program
5. Execute `main_menu()` to start using the interface

## 7. Reflection and Design Justification

This implementation required careful attention to algorithmic thinking. Searching, sorting, and validation routines were implemented manually to demonstrate understanding of fundamental principles. Python’s in-built flexibility allowed for readable, structured code while maintaining the restrictions of no external libraries.

All code is commented for clarity. Key design decisions, such as storing timestamps using ISO format and limiting tags to five, stem from the original PHP design in Part 1. Bubble sort was chosen for simplicity and alignment with the algorithms studied (Knuth, 1997).

## 8. Academic Integrity

All code was written by the student, following the design principles established in Part 1. No third-party libraries or code generation tools were used. References are included below.

## 9. References

- Cormen, T.H., Leiserson, C.E., Rivest, R.L. and Stein, C., 2009. *Introduction to Algorithms*. 3rd ed. MIT Press.
- Knuth, D.E., 1997. *The Art of Computer Programming, Volume 3: Sorting and Searching*. 2nd ed. Addison-Wesley.
- Russell, S. and Norvig, P., 2010. *Artificial Intelligence: A Modern Approach*. 3rd ed. Pearson.