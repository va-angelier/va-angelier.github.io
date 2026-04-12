from graphviz import Digraph

dot = Digraph("sqli_flow", format="png", engine="dot")
dot.attr(rankdir="TB", fontsize="12", fontname="Arial")

# Nodes
dot.node("S", "Start", shape="oval")
dot.node("A", "Application requires\ndatabase interaction")
dot.node("B", "User input accepted")
dot.node("C", "User input concatenated\ndirectly into SQL query")
dot.node("D", "Decision:\nInput validated/\nsanitised?", shape="diamond", style="filled", fillcolor="lightyellow")

dot.node("E1", "Secure path:\nparameterised queries / ORM", style="filled", fillcolor="lightgreen")
dot.node("F1", "End: No weakness", shape="oval", style="filled", fillcolor="lightgreen")

dot.node("E2", "No parameterised queries\n(prepared statements omitted)", style="filled", fillcolor="lightcoral")
dot.node("F2", "Decision:\nSecurity review\nperformed?", shape="diamond", style="filled", fillcolor="lightyellow")
dot.node("G1", "Secure path:\nissue fixed before release", style="filled", fillcolor="lightgreen")
dot.node("H1", "End: No weakness", shape="oval", style="filled", fillcolor="lightgreen")

dot.node("G2", "Deploy to production", style="filled", fillcolor="lightcoral")
dot.node("H2", "Exploitation:\nattacker injects malicious input", style="filled", fillcolor="lightcoral")
dot.node("I2", "End: Injection exploited\n(e.g., data breach)", shape="oval", style="filled", fillcolor="lightcoral")

# Edges
dot.edges([("S", "A"), ("A", "B"), ("B", "C"), ("C", "D")])

dot.edge("D", "E1", label="Yes")
dot.edge("E1", "F1")

dot.edge("D", "E2", label="No")
dot.edge("E2", "F2")

dot.edge("F2", "G1", label="Yes")
dot.edge("G1", "H1")

dot.edge("F2", "G2", label="No")
dot.edge("G2", "H2")
dot.edge("H2", "I2")

# Render
png_path = dot.render("sqli_injection_flowchart", cleanup=True, view=True)
dot.format = "svg"
svg_path = dot.render("sqli_injection_flowchart_svg", cleanup=True, view=True)

print("Generated:", png_path, "and", svg_path)