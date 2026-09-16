from visual_teaching_toolkit.music import NOTE_TO_PC


def test_enharmonic_pitch_classes():
    assert NOTE_TO_PC["C#"] == NOTE_TO_PC["Db"]
    assert NOTE_TO_PC["D#"] == NOTE_TO_PC["Eb"]
    assert NOTE_TO_PC["F#"] == NOTE_TO_PC["Gb"]
    assert NOTE_TO_PC["G#"] == NOTE_TO_PC["Ab"]
    assert NOTE_TO_PC["A#"] == NOTE_TO_PC["Bb"]


def test_d_dorian_pitch_classes():
    pcs = [NOTE_TO_PC[n] for n in ["D", "E", "F", "G", "A", "B", "C"]]
    root = NOTE_TO_PC["D"]
    distances = sorted((pc - root) % 12 for pc in pcs)
    assert distances == [0, 2, 3, 5, 7, 9, 10]


def test_standard_tuning_known_positions():
    e = NOTE_TO_PC["E"]
    assert (e + 3) % 12 == NOTE_TO_PC["G"]
    assert (e + 5) % 12 == NOTE_TO_PC["A"]
    assert (e + 10) % 12 == NOTE_TO_PC["D"]
