Methods

Class: Chip
- fill_grid
- load_gates
- load_connections
- add_wire
- calculate_costs

Class: Gate
- get_id
- get_x
- get_y
- get_coords
- add_destination
- get_destination

Class: Wire
- add_unit
- pop_unit
- reset_path
- get_path
- get_current_position
- get_previous_position
- check_for_father

Class: Grid
- get_grid_size
- initialize_grid
- check_for_illegal_gate
- visualize_grid