// BitSetCAPI.cpp ---
// Filename: BitSetCAPI.cpp
// Author: Abhishek Udupa
// Created: Mon Oct  5 00:22:51 2015 (-0400)
//
// Copyright (c) 2013, Abhishek Udupa, University of Pennsylvania
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
// 3. All advertising materials mentioning features or use of this software
//    must display the following acknowledgement:
//    This product includes software developed by The University of Pennsylvania
// 4. Neither the name of the University of Pennsylvania nor the
//    names of its contributors may be used to endorse or promote products
//    derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ''AS IS'' AND ANY
// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//

// Code:

#include <exception>
#include "BitSet.hpp"
#include "LibEUSolver.h"

static std::string s_bitset_c_api_output_buffer_;
static std::string s_libeusolver_c_api_error_buffer_;

#define BEGIN_CHECKED_BLOCK_                     \
    s_libeusolver_c_api_error_buffer_.clear();   \
    try {                                        \
        (void)0

#define END_CHECKED_BLOCK_                                           \
    } catch(const std::exception& e) {                               \
        s_libeusolver_c_api_error_buffer_ = std::string(e.what());   \
    } (void)0

static inline eusolver::BitSet* as_bs(void* ptr)
{
    return static_cast<eusolver::BitSet*>(ptr);
}

static inline const eusolver::BitSet* as_bs(const void* ptr)
{
    return static_cast<const eusolver::BitSet*>(ptr);
}

void* eus_bitset_construct(u64 size_of_universe, bool initial_value)
{
    BEGIN_CHECKED_BLOCK_;
    return new eusolver::BitSet(size_of_universe, initial_value);
    END_CHECKED_BLOCK_;
    return nullptr;
}

void eus_bitset_destroy(void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    delete as_bs(bitset);
    END_CHECKED_BLOCK_;
}

bool eus_bitsets_equal(const void* bitset1, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    return ((*(as_bs(bitset1))) == (*(as_bs(bitset2))));
    END_CHECKED_BLOCK_;
    return false;
}

bool eus_bitsets_not_equal(const void* bitset1, const void* bitset2)
{
    return (!(eus_bitsets_equal(bitset1, bitset2)));
}

bool eus_bitset_is_proper_subset(const void* bitset1, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    return ((*(as_bs(bitset1))) < (*(as_bs(bitset2))));
    END_CHECKED_BLOCK_;
    return false;
}

bool eus_bitset_is_subset(const void* bitset1, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    return ((*(as_bs(bitset1))) <= (*(as_bs(bitset2))));
    END_CHECKED_BLOCK_;
    return false;
}

bool eus_bitset_is_proper_superset(const void* bitset1, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    return ((*(as_bs(bitset1))) > (*(as_bs(bitset2))));
    END_CHECKED_BLOCK_;
    return false;
}

bool eus_bitset_is_superset(const void* bitset1, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    return ((*(as_bs(bitset1))) >= (*(as_bs(bitset2))));
    END_CHECKED_BLOCK_;
    return false;
}

void eus_bitset_set_bit(void* bitset, u64 bit_num)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset)->set_bit(bit_num);
    END_CHECKED_BLOCK_;
}

void eus_bitset_clear_bit(void* bitset, u64 bit_num)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset)->clear_bit(bit_num);
    END_CHECKED_BLOCK_;
}

bool eus_bitset_flip_bit(void* bitset, u64 bit_num)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->flip_bit(bit_num);
    END_CHECKED_BLOCK_;
    return false;
}

bool eus_bitset_test_bit(const void* bitset, u64 bit_num)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->test_bit(bit_num);
    END_CHECKED_BLOCK_;
    return false;
}

void eus_bitset_set_all(void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset)->set_all();
    END_CHECKED_BLOCK_;
}

void eus_bitset_clear_all(void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset)->clear_all();
    END_CHECKED_BLOCK_;
}

void eus_bitset_flip_all(void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset)->flip_all();
    END_CHECKED_BLOCK_;
}

u64 eus_bitset_get_size_of_universe(const void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->get_size_of_universe();
    END_CHECKED_BLOCK_;
    return 0;
}

u64 eus_bitset_get_length(const void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->length();
    END_CHECKED_BLOCK_;
    return 0;
}

bool eus_bitset_is_full(const void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->is_full();
    END_CHECKED_BLOCK_;
    return false;
}

bool eus_bitset_is_empty(const void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->is_empty();
    END_CHECKED_BLOCK_;
    return false;
}

void* eus_bitset_and_functional(const void* bitset1, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset1)->intersection_with(as_bs(bitset2));
    END_CHECKED_BLOCK_;
    return nullptr;
}

void* eus_bitset_or_functional(const void* bitset1, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset1)->union_with(as_bs(bitset2));
    END_CHECKED_BLOCK_;
    return nullptr;
}

void* eus_bitset_xor_functional(const void* bitset1, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset1)->symmetric_difference_with(as_bs(bitset2));
    END_CHECKED_BLOCK_;
    return nullptr;
}

void* eus_bitset_minus_functional(const void* bitset1, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset1)->difference_with(as_bs(bitset2));
    END_CHECKED_BLOCK_;
    return nullptr;
}

void* eus_bitset_negate_functional(const void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->negate();
    END_CHECKED_BLOCK_;
    return nullptr;
}

void eus_bitset_inplace_and(void* bitset1_and_result, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset1_and_result)->intersect_with_in_place(as_bs(bitset2));
    END_CHECKED_BLOCK_;
}

void eus_bitset_inplace_or(void* bitset1_and_result, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset1_and_result)->union_with_in_place(as_bs(bitset2));
    END_CHECKED_BLOCK_;
}

void eus_bitset_inplace_xor(void* bitset1_and_result, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset1_and_result)->symmetric_difference_with_in_place(as_bs(bitset2));
    END_CHECKED_BLOCK_;
}

void eus_bitset_inplace_minus(void* bitset1_and_result, const void* bitset2)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset1_and_result)->difference_with_in_place(as_bs(bitset2));
    END_CHECKED_BLOCK_;
}

void eus_bitset_inplace_negate(void* bitset_and_result)
{
    BEGIN_CHECKED_BLOCK_;
    as_bs(bitset_and_result)->negate_in_place();
    END_CHECKED_BLOCK_;
}

i64 eus_bitset_get_next_element_greater_than_or_equal_to(const void* bitset, u64 position)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->get_next_element_greater_than_or_equal_to(position);
    END_CHECKED_BLOCK_;
    return 0;
}

i64 eus_bitset_get_next_element_greater_than(const void* bitset, u64 position)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->get_next_element_greater_than(position);
    END_CHECKED_BLOCK_;
    return 0;
}

i64 eus_bitset_get_prev_element_lesser_than_or_equal_to(const void* bitset, u64 position)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->get_prev_element_lesser_than_or_equal_to(position);
    END_CHECKED_BLOCK_;
    return 0;
}

i64 eus_bitset_get_prev_element_lesser_than(const void* bitset, u64 position)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->get_prev_element_lesser_than(position);
    END_CHECKED_BLOCK_;
    return 0;
}

u64 eus_bitset_get_hash(const void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->hash();
    END_CHECKED_BLOCK_;
    return 0;
}

const char* eus_bitset_to_string(const void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    s_bitset_c_api_output_buffer_ = as_bs(bitset)->to_string();
    return s_bitset_c_api_output_buffer_.c_str();
    END_CHECKED_BLOCK_;
    return nullptr;
}

void* eus_bitset_clone(const void* bitset)
{
    BEGIN_CHECKED_BLOCK_;
    return as_bs(bitset)->clone();
    END_CHECKED_BLOCK_;
    return nullptr;
}

bool eus_check_error()
{
    return (s_libeusolver_c_api_error_buffer_.length() > 0);
}

const char* eus_get_last_error_string()
{
    if (eus_check_error()) {
        return s_libeusolver_c_api_error_buffer_.c_str();
    } else {
        return nullptr;
    }
}

//
// BitSetCAPI.cpp ends here
