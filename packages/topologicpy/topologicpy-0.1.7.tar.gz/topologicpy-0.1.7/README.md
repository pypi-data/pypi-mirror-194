<img src="https://topologic.app/wp-content/uploads/2023/02/topologicpy-logo-no-loop.gif" alt="topologicpy logo" width="250" loop="1">

# Topologic - A Hierarchical and Topological Modelling Library for Architecture

## Introduction
Topologic is a powerful software modelling library that enables hierarchical and topological representations of architectural spaces, buildings, and artefacts through non-manifold topology (NMT). It is designed as a core python library with additional optional plugins for visual data flow programming (VDFP) applications and parametric modelling platforms commonly used in architectural design practice. Users can use either visual programming nodes and connections or scripting to interact with Topologic and perform various architectural design and analysis tasks.

Topologic's topological consistency allows it to create a lightweight representation of a building as an external envelope and the subdivision of the enclosed space into separate spaces and zones using zero-thickness internal surfaces. This means that a user can query these cellular spaces and surfaces regarding their connectivity and conduct various analyses. For example, this lightweight and consistent representation is well-suited for energy analysis simulation software's input data requirements.

In addition to topological consistency, Topologic also supports the process of "defeaturing". Defeaturing is an essential step in converting building information models to models suitable for analysis. It involves simplifying the geometry of a model by removing small or unnecessary details that are not needed for analysis. Defeaturing allows for faster and more accurate analysis by reducing the complexity of the model, while preserving its overall topological consistency.

Furthermore, Topologic allows entities with mixed dimensionalities and those that are optionally independent to co-exist, enabling structural models to be represented in a coherent manner. For instance, lines can represent columns and beams, surfaces can represent walls and slabs, and volumes can represent solids. Even non-building entities like structural loads can be efficiently attached to the structure. This approach creates a lightweight model that is well-matched with the input data requirements for structural analysis simulation software.
