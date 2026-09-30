#ifndef PIPE_LIVE27_SEQUENCE_H
#define PIPE_LIVE27_SEQUENCE_H
// Fixture-only precommitted observations; not public wire declarations.
struct Expected27 { unsigned opcode, admission, status; };
static const Expected27 expected27[] = {
    {4096, 0, 0}, // request 1
    {4101, 1, 0}, // request 2
    {34, 2, 0}, // request 3
    {56, 3, 0}, // request 4
    {14, 4, 0}, // request 5
    {53, 5, 0}, // request 6
    {30, 6, 0}, // request 7
    {31, 7, 0}, // request 8
    {29, 8, 0}, // request 9
    {27, 9, 0}, // request 10
    {35, 10, 0}, // request 11
    {19, 11, 0}, // request 12
    {35, 12, 0}, // request 13
    {19, 13, 0}, // request 14
    {26, 14, 0}, // request 15
    {30, 15, 3}, // request 16
    {19, 15, 2}, // request 17
    {26, 16, 2}, // request 18
    {19, 17, 0}, // request 19
    {52, 18, 0}, // request 20
    {26, 18, 4097}, // request 21
    {4109, 19, 0}, // request 22
};
#endif
