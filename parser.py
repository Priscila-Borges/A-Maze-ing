from dataclasses import dataclass


@dataclass
class Config:
    width: int
    height: int
    maze_entry: tuple[int, int]
    maze_exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def read_config_file(read_file_path: str) -> dict[str, str]:
    raw_data: dict[str, str] = {}

    with open(read_file_path, "r") as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Syntax error on line {line_num}: "
                                 f"missing '='")

            key, value = line.split("=", 1)
            raw_data[key.strip()] = value.strip()

    return raw_data


def parse_config(file_path: str) -> Config:
    raw_data = read_config_file(file_path)

    seed = None
    if "SEED" in raw_data and raw_data["SEED"]:
        try:
            seed = int(raw_data["SEED"])
        except ValueError:
            raise ValueError("SEED must be an integer")

    required_keys = {
                     "WIDTH",
                     "HEIGHT",
                     "ENTRY",
                     "EXIT",
                     "OUTPUT_FILE",
                     "PERFECT"
    }

    missing_keys = required_keys - raw_data.keys()
    if missing_keys:
        raise ValueError("Missing mandatory keys")

    try:
        width = int(raw_data["WIDTH"])
        height = int(raw_data["HEIGHT"])
    except ValueError:
        raise ValueError("WIDTH and HEIGHT must be valid integers.")

    if width <= 1 or height <= 1:
        raise ValueError("WIDTH and HEIGHT must be greater than 1.")

    m_entry = raw_data["ENTRY"]
    m_exit = raw_data["EXIT"]

    try:
        x_entry, y_entry = m_entry.split(",")
        x_exit, y_exit = m_exit.split(",")
    except ValueError:
        raise ValueError("ENTRY and EXIT must be formated as x, y")

    try:
        maze_entry: tuple[int, int] = (int(x_entry), int(y_entry))
        maze_exit: tuple[int, int] = (int(x_exit), int(y_exit))
    except ValueError:
        raise ValueError("ENTRY and EXIT must be a positive integer")

    if not (0 <= maze_entry[0] < width and 0 <= maze_entry[1] < height):
        raise ValueError("ENTRY coordinates is out of grid bounds")
    if not (0 <= maze_exit[0] < width and 0 <= maze_exit[1] < height):
        raise ValueError("EXIT coordinates is out of grid bounds")

    if maze_entry == maze_exit:
        raise ValueError("ENTRY and EXIT coordanates cannot be identical")

    perfect_raw = raw_data["PERFECT"].lower()
    if perfect_raw not in ("true", "false"):
        raise ValueError("Perfect must be True or False")
    perfect = perfect_raw == "true"

    output_file = raw_data["OUTPUT_FILE"]
    if not output_file:
        raise ValueError("OUTPUT_FILE cannot be empty")

    try:
        output_file = str(output_file)
    except ValueError:
        raise ValueError("OUTPUT_FILE must be a string")

    return Config(
        width=width,
        height=height,
        maze_entry=maze_entry,
        maze_exit=maze_exit,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
