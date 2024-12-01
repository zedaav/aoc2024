use regex::Regex;
use std::fs;

fn step1(template: &str) {
    // Prepare regex
    let re = Regex::new("(\\d+) +(\\d+)").unwrap();

    // Read inputs
    let input = fs::read_to_string(format!("inputs/d01.{}.txt", template)).unwrap();

    // Parse numbers
    let mut nbs1: Vec<u64> = Vec::new();
    let mut nbs2: Vec<u64> = Vec::new();
    for (_, [nb1, nb2]) in re.captures_iter(&input).map(|c| c.extract()) {
        nbs1.push(nb1.parse::<u64>().unwrap());
        nbs2.push(nb2.parse::<u64>().unwrap());
    }

    // Sort them
    nbs1.sort();
    nbs2.sort();

    // Iterate
    let mut total: u64 = 0;
    for (nb1, nb2) in std::iter::zip(nbs1, nbs2) {
        // Add "distances"
        total += nb1.abs_diff(nb2);
    }
    println!("Solution for {}: {}", template, total);
}

fn main() {
    step1("sample");
    step1("input");
}
