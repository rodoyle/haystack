extern crate haystack;
extern crate fnv;

use fnv::FnvHashMap;
use haystack::LFmer;
use std::ops::AddAssign;


#[test]
fn str_to_vec() {
    let text: &str = "mississippi"; // Classic BWT String
    let length = text.len();
    let mut counter = FnvHashMap::<char, u8>::default();
    
    let mut vector: Vec<LFmer> = Vec::with_capacity(length);
    // we know the first char will wrap to our mock terminator
    let mut l_rank = 1;
    let mut l_mer = '$';
    for (text_pos, f_mer) in text.char_indices() {
        let f_rank = counter.entry(f_mer)
            .or_insert(0);
        f_rank.add_assign(1);
        println!("idx = {}, T = {} Rank = {}", text_pos, f_mer, f_rank);
        let lfmer = LFmer {
            text_pos,
            l_rank,
            l_mer,
            f_mer,
            f_rank: *f_rank,
        };
        vector.push(lfmer);
        // Update for next char
        l_rank = *f_rank;
        l_mer = f_mer;
    }
    vector.sort();

}
/// Test we take a utf-8 string and convert
/// it's bytes into a vector
#[test]
fn text_to_vec() {
    let text: &str = "Founded in 1952 and incorporated in 1957, Bio-Rad Laboratories, Inc. (referred to in this report as “Bio-Rad,”
“we,” “us,” and “our”) was initially engaged in the development and production of specialty chemicals used in
biochemical, pharmaceutical and other life science research applications.";
    
    let bytes = text.as_bytes();

    


}
