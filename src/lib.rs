
/// Experimental struct for combining
/// techniques of Ngram and BWT/LFMapping
/// for encoding byte string
/// The L and F mers and their ranks must be unique to have a 
/// Lossless mapping
#[derive(Debug, Eq)]
pub struct LFmer {
    // pub document_id; We track the source text for this record
    /// Position in the Text. We might need this for sorting.
    /// Alternatively it should go separately but alongside
    /// the main tuple
    pub text_pos: usize,
    /// the prior k-mer constructed from the first k elements of the prior suffix
    /// Maps to the L column in a LF mapping
    pub l_mer: char,
    /// the rank (occurence) of the prior k-mer
    /// IN THE TEXT (nth- instance of k-mer as read
    pub l_rank: u8,
    /// the CURRENT k-mer from the current suffix
    /// Maps to the F column in a LF mapping
    pub f_mer: char,
    /// the rank (occurence) of the prior k-mer
    /// IN THE TEXT (nth- instance of k-mer as read
    pub f_rank: u8,
}
/// The implementations of PartialEq and PartialOrd are extremely important
/// for how these structs get used
impl PartialEq for LFmer {
    fn eq(&self, other: &Self) -> bool {
        self.l_mer == other.l_mer &&
            self.l_rank == other.l_rank &&
            self.f_mer == other.f_mer &&
            self.f_rank == other.f_rank
    }
}
use std::cmp::Ordering;

impl PartialOrd for LFmer {
 /// We sort LF entries by the F-mer (the first column)
 /// Technically if there is a tie we should extend K until the tie is broken or we reach the end
 /// of the input text
 fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
    self.f_mer.partial_cmp(&other.f_mer)
 }
}

impl Ord for LFmer {
 // Ord implies a stable sort order (total ordering) such that ties are resolved
 // consistently and unabiguosly
 // In situations where we want to be able to exactly reconstruct the original texts in
 // the exact original order, we need to track enough data to resolve these ties exactly
 // In practice this means we need to extend the F-mer (suffix) to the end of the text
 // and track a unique id for the source text
 // 
 // Alternatively, we can track the exact rank of each F and L mer. This has the effect of
 // providing extra data which will disambiguate the L-F mapping exactly.
 //
 // However there is still the matter of getting the order right for searching.
 //
 // For classification, clustering, or recombination we don't really need to be that precise
 // and it's sufficient to trim the F-mer after K entries
 fn cmp(&self, other: &Self) -> Ordering {
    self.f_mer.cmp(&other.f_mer)
 }
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
