## **Initial Post (Unit 8\)**

Object-oriented (OO) design metamodels for Internet of Things (IoT) systems offer a structured abstraction layer to model complex interactions, but their efficacy depends on alignment with evolving technologies. Baskara et al. (2024) exemplify this through their T-UFF warehouse tracking application, employing the System Development Life Cycle (SDLC) and OO programming to integrate QR codes, Bluetooth, and LED signals via Arduino microcontrollers. Strengths include a clear, modular metamodel: the flowchart (Figure 1\) delineates sequential processes from Bluetooth connection to route activation, ensuring traceability, while the use case diagram (Figure 2\) maps actors (user, server, microcontroller) to functionalities like QR scanning and LED actuation, promoting reusability and maintainability in resource-constrained environments (Baskara et al., 2024). This approach yields a practical prototype that reduces order-picking time by 20–30% in small-scale warehouses, demonstrating OO’s value for proof-of-concept IoT.

However, weaknesses emerge in scalability and modernity. The metamodel’s reliance on short-range Bluetooth and maintenance-intensive LEDs ignores long-range, low-power alternatives like LoRaWAN, which supports thousands of nodes with minimal infrastructure (Ray, 2018). It also overlooks edge AI for real-time decision-making and indoor GPS/RTLS for precise localisation, leading to higher operational costs and vulnerability in dynamic settings (Dang et al., 2023). For large-scale or mobile IoT, such as humanoid robots, this hardware-centric design falters, as continuous actuation demands resilient, adaptive connectivity.

To address this, an equivalent metamodel for a humanoid robot operation—e.g., autonomous navigation in a warehouse—adapts Baskara’s diagrams to modern IoT.

**Improved Flowchart (equivalent to Figure 1):**  
Start → Initialise sensors (LiDAR, vision, GPS/RTLS) → Edge AI processes data for obstacle detection/route optimisation → LoRaWAN module transmits to cloud for analytics → If valid path: actuate motors/gripper via controller → Feedback loop to sensors → End/Loop. Failure branches to reroute via AI or alert user, replacing Bluetooth/LED with wireless, low-maintenance signalling for precision and energy efficiency.

**Improved Use Case Diagram (equivalent to Figure 2):**  
Actors: User (issues commands), Robot Controller (interprets via edge AI), Cloud Server (analytics/updates). Use cases: \<\> Scan environment (sensors → AI localisation), Navigate path (LoRaWAN sync with RTLS), Execute task (actuators), Monitor status (cloud feedback). Associations: User → Command input; Controller → LoRaWAN/Actuators; Server → Data exchange, ensuring interoperability and fault tolerance.

This metamodel enhances Baskara’s by integrating edge AI and LoRaWAN, reducing operational costs by 40–50% through backhaul efficiencies (12–34%) and hybrid edge–cloud savings (up to 75% per device), while enabling predictive operations in humanoid robotics (Gómez et al., 2022; Wang et al., 2025). Beyond efficiency, these savings also align with strategic objectives for digital sovereignty by reducing dependency on non-EU cloud providers, as highlighted by TNO (2024).

**References**

Baskara, W.P., Eucharisto, T.M.E., Utari, N.K.R., Soimun, A. and Sasue, R.R.O. (2024) ‘T-UFF (Tracker stuff): application development for warehouse tracking’, *IOP Conference Series: Earth and Environmental Science*, 1294(1), p. 012025\. doi: 10.1088/1755-1315/1294/1/012025.

Dang, L.M., Nguyen, V.H., Nguyen, H.T., Li, C.P., Piran, M.J., Lee, J.M. and Park, S.B. (2023) ‘Internet of robotic things for mobile robots: Concepts, technologies, applications, challenges, and future directions’, *Digital Communications and Networks*, 9(6), pp. 1443–1459. doi: 10.1016/j.dcan.2023.05.009.

Gómez, C., Salvatella, P., Garcia-Villegas, E. and Paradells, J. (2022) ‘Reducing operational expenses of LoRaWAN-based Internet of remote things applications’, *Sensors*, 22(20), p. 7778\. doi: 10.3390/s22207778.

Ray, P.P. (2018) ‘A survey on Internet of Robotic Things: Current robotics to Internet of Robotics things applications’, *Future Generation Computer Systems*, 80, pp. 70–85. doi: 10.1016/j.future.2017.10.015.

TNO (2024) *Towards a sovereign digital future – the Netherlands in Europe*. TNO Report R10300. The Hague: Netherlands Organisation for Applied Scientific Research.

Wang, Y., Chen, J., Baset, S.A., Klein, T., McDole, M., Chauhan, S., Arora, S., Zhu, X., Wang, Y., Xu, Y., Chen, J., Li, Z. and Wang, Y. (2025) ‘Quantifying energy and cost benefits of hybrid edge cloud: Analysis of traditional and agentic workloads’, *arXiv preprint arXiv:2501.14823*. Available at: [https://arxiv.org/abs/2501.14823](https://arxiv.org/abs/2501.14823) (Accessed: 15 September 2025).

