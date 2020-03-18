#pragma once
#include <stdbool.h>


#ifdef  __cplusplus
extern "C" {
#endif
bool check_rectangle(int *pos1, int *diag1, int *pos2, int *diag2);
bool is_balans(float *pos1, float *pos2, float *diag2);
bool check_line_intersect(int line[4], int face[4]);
}