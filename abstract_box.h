#pragma once
#include <array>

class AbstractBox
{
    private:
        std::array<int,3> position;
        std::array<int,3> diag;
        int id;
        int rotation_sate;
        int rotation_variants;
        bool is_rotatableX;
        bool is_rotatableY;
        bool is_rotatableZ;
        
    
    public:
        static int boxes_count;
        std::array<int,3> get_position();
        std::array<int,3> get_diag();
        int get_id();
        void set_position(std::array<int,3> &position);
        void set_diag(std::array<int,3> &diag);
        void putOnPos(std::array<int,3> &pos);
        AbstractBox();
        AbstractBox(std::array<int,3> &diag, std::array<bool,3> &is_rotatableXYZ);
};