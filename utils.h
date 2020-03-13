#pragma once

bool check_rects_intersect(std::array<int,2> &pos1, std::array<int,2> &diag1, 
                        std::array<int,2> &pos2, std::array<int,2> &diag2);
bool dot_inside_rect(float *pos1, float *pos2, float *diag2);
bool check_lines_intersect(std::array<int,2> &line1, std::array<int,2> &line2);
bool check_line_face_intersect(int line[2][2], int face[2][2]);
