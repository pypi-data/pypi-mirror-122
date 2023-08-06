#![allow(dead_code)]
use ahash::AHasher;
use rand;
use std::hash::{Hash, Hasher};
use std::io::{Error, ErrorKind};
use std::marker::PhantomData;

#[derive(Clone)]
struct Row<T: Hash + Clone> {
    data: Vec<u64>,
    width: u64,
    a: u128,
    b: u128,
    p: PhantomData<T>,
}

impl<T: Hash + Clone> Row<T> {
    fn new(w: u64) -> Row<T> {
        let a = rand::random::<u128>();
        let b = rand::random::<u128>();
        //let hasher = AHasher::new_with_keys(a, b);
        Row {
            data: vec![0u64; w as usize],
            width: w,
            a: a,
            b: b,
            p: PhantomData,
        }
    }
    fn hash(&self, t: T) -> u64 {
        let mut h = AHasher::new_with_keys(self.a, self.b);
        //let mut h = self.hasher.clone();
        t.hash(&mut h);
        h.finish() % self.width as u64
    }

    fn insert(&mut self, t: T) -> u64 {
        let col = self.hash(t) as usize;
        self.data[col] += 1;
        self.data[col]
    }
    fn add(&mut self, t: T, n: u64) -> u64 {
        let col = self.hash(t) as usize;
        self.data[col] += n;
        self.data[col]
    }

    fn retrieve(&self, t: T) -> u64 {
        let col = self.hash(t) as usize;
        self.data[col]
    }
    fn clear(&mut self) {
        self.data = vec![0u64; self.width as usize]
    }
    //scale multiplies all values in the row by factor
    fn scale(&mut self, factor: f64) {
        self.data
            .iter_mut()
            .for_each(|i| *i = (factor * (*i as f64)).floor() as u64)
    }

    fn combine(&mut self, other: &Row<T>) -> Result<(), Error> {
        if other.a != self.a {
            let custom_error = Error::new(
                ErrorKind::Other,
                "hash init parameters don't match - was one CMS cloned from the other?",
            );
            return Err(custom_error);
        }
        for i in 0..self.width as usize {
            self.data[i] = self.data[i] + other.data[i];
        }

        Ok(())
    }
}
/// CMS is a count-min-sketch streaming data structure
#[derive(Clone)]
pub struct CountMinSketch<T: Hash + Clone> {
    rows: Vec<Row<T>>,
    width: u64,
    depth: u64,
}

impl<T: Hash + Clone> CountMinSketch<T> {
    ///new creates a new CMS struct
    pub fn new(depth: u64, width: u64) -> CountMinSketch<T> {
        Self {
            rows: (0..depth).map(|_| Row::new(width)).collect(),
            width,
            depth,
        }
    }
    ///new_with_probs creates a new CMS s.t. error is less
    ///than tol with probability 1-p_err for capacity unique entries
    pub fn new_with_probs(tol: f64, p_err: f64, capacity: usize) -> CountMinSketch<T> {
        let width = (1.0f64.exp() / (tol / capacity as f64)) as u64;
        let depth = (1.0 / p_err).ln() as u64;
        Self::new(depth, width)
    }
    ///new_from_cms generates a new CMS matching an existing one
    ///this allows combining counts from different CMS structures
    pub fn new_from_cms(other: &CountMinSketch<T>) -> CountMinSketch<T> {
        let mut n = other.clone();
        n.clear();
        n
    }

    ///insert a new value or increase the count of an existing one
    pub fn insert(&mut self, t: T) -> u64 {
        self.rows
            .iter_mut()
            .map(|row| row.insert(t.clone()))
            .min()
            .unwrap()
    }
    ///retrieve the estimated count for a value
    pub fn retrieve(&self, t: T) -> u64 {
        //note - this can never panic, there is guaranteed to be data
        self.rows
            .iter()
            .map(|row| row.retrieve(t.clone()))
            .min()
            .unwrap()
    }
    ///clear out the structure
    pub fn clear(&mut self) {
        self.rows.iter_mut().for_each(|row| row.clear());
    }
    ///scale the cms by factor
    pub fn scale(&mut self, factor: f64) {
        self.rows.iter_mut().for_each(|row| row.scale(factor));
    }
    ///combine the CMS with another one (must be a clone or built with new_from)
    pub fn combine(&mut self, other: &CountMinSketch<T>) -> Result<(), Error> {
        self.rows
            .iter_mut()
            .zip(other.rows.iter())
            .try_for_each(|(rowa, rowb)| rowa.combine(&rowb))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_add_retrieve_row() {
        let mut r: Row<u64> = Row::new(1000);
        for i in 0..100 {
            r.insert(i);
        }
        println!("retrieved {}", r.retrieve(10));
        assert!(r.retrieve(10) < 3);
    }

    #[test]
    fn test_row_clear() {
        let mut r: Row<u64> = Row::new(100);
        for i in 0..100 {
            r.insert(i);
        }
        r.clear();
        assert_eq!(0, r.retrieve(10))
    }
    #[test]
    fn test_row_scale() {
        let mut r: Row<u64> = Row::new(100);
        for _ in 0..100 {
            r.insert(0);
        }
        r.scale(0.5);
        println!("got {}", r.retrieve(0));
        assert_eq!(50, r.retrieve(0))
    }
    #[test]
    fn test_row_combine() {
        let mut r: Row<u64> = Row::new(100);
        let mut s: Row<u64> = Row::new(100);
        let mut t = r.clone();
        for _ in 0..100 {
            r.insert(10);
        }
        //this should error - the keys will not be the same
        s.combine(&r).expect_err("Expecting CopyError");
        //this will not error because t is cloned from r
        assert_eq!(0, t.retrieve(10));

        t.combine(&r).unwrap();
        assert_eq!(100, t.retrieve(10))
    }
    #[test]
    fn test_cms_add_retrieve() {
        let mut cms: CountMinSketch<u64> = CountMinSketch::new(1000, 1000);
        for i in 1..1001 {
            assert_eq!(i, cms.insert(10))
        }
        assert_eq!(1000, cms.retrieve(10))
    }
    #[test]
    fn test_cms_add_retrieve_mult() {
        let mut cms: CountMinSketch<u64> = CountMinSketch::new_with_probs(0.1, 0.00001, 100);
        for i in 0..1_000_000 {
            cms.insert(i % 100);
        }
        (0..100).for_each(|key| assert!(cms.retrieve(key) >= 10_000));
        (0..100).for_each(|i| assert!(cms.retrieve(i) < 11_000));
    }
    #[test]
    fn test_cms_clear() {
        let mut cms: CountMinSketch<u64> = CountMinSketch::new(1000, 1000);
        for i in 0..100 {
            cms.insert(i);
        }
        cms.clear();
        assert_eq!(0, cms.retrieve(10))
    }

    #[test]
    fn test_cms_scale() {
        let mut cms: CountMinSketch<u64> = CountMinSketch::new_with_probs(0.1, 0.00001, 100);
        for _ in 0..100 {
            cms.insert(0);
        }
        cms.scale(0.5);
        println!("got {}", cms.retrieve(0));
        assert_eq!(50, cms.retrieve(0))
    }
    #[test]
    fn test_cms_combine() {
        let mut cms_a: CountMinSketch<u64> = CountMinSketch::new_with_probs(0.1, 0.00001, 100);
        let mut cms_b: CountMinSketch<u64> = CountMinSketch::new_with_probs(0.1, 0.00001, 100);
        let mut cms_c = cms_a.clone();
        for _ in 0..100 {
            cms_a.insert(10);
        }
        //this should error - the keys will not be the same
        cms_b.combine(&cms_a).expect_err("Expecting CopyError");
        //this will not error because t is cloned from r
        assert_eq!(0, cms_c.retrieve(10));

        cms_c.combine(&cms_a).unwrap();
        assert_eq!(100, cms_c.retrieve(10))
    }
}
