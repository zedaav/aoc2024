use regex::Regex;
use std::{
    collections::{HashMap, HashSet},
    fs,
};

struct Robot {
    p: (i32, i32),
    v: (i32, i32),
    dims: (i32, i32),
}

impl Robot {
    // Move robot
    fn mv(&self, iters: i32) -> (i32, i32) {
        let (mut x, mut y) = self.p;
        let (dx, dy) = self.v;
        let (w, h) = self.dims;

        // Move be specified iterations
        x += dx * iters;
        x %= w;
        x += if x < 0 { w } else { 0 };
        y += dy * iters;
        y %= h;
        y += if y < 0 { h } else { 0 };
        (x, y)
    }
}

fn parse(template: &str, dims: (i32, i32)) -> Vec<Robot> {
    // Prepare regex
    let re = Regex::new("p=([-\\d]+),([-\\d]+) +v=([-\\d]+),([-\\d]+)").unwrap();

    // Read inputs
    let input = fs::read_to_string(format!("inputs/d14.{}.txt", template)).unwrap();

    // Parse robots
    let mut robots: Vec<Robot> = Vec::new();
    for (_, [nb1, nb2, nb3, nb4]) in re.captures_iter(&input).map(|c| c.extract()) {
        robots.push(Robot {
            p: (nb1.parse::<i32>().unwrap(), nb2.parse::<i32>().unwrap()),
            v: (nb3.parse::<i32>().unwrap(), nb4.parse::<i32>().unwrap()),
            dims,
        });
    }

    return robots;
}

fn step1(template: &str, dims: (i32, i32)) {
    // Parse robots
    let robots = parse(template, dims);

    // Iterate on robots
    let (w, h) = dims;
    let (qw, qh) = (w / 2, h / 2);
    let mut quarters: HashMap<(u32, u32), u32> = HashMap::new();
    for r in &robots {
        // Move by 100 iterations
        let (x, y) = r.mv(100);
        if (x == qw) || (y == qh) {
            // Just in the middle, don't count
            continue;
        }

        // Put in the right quarter
        let (qx, qy) = ((x > qw) as u32, (y > qh) as u32);
        quarters.insert((qx, qy), quarters.get(&(qx, qy)).unwrap_or(&0) + 1);
    }

    // Multiply all quarters lengths
    let mut total = 1;
    for (_, v) in quarters {
        total *= v;
    }
    println!("Solution 1 for {}: {}", template, total);
}

fn step2(template: &str, dims: (i32, i32)) {
    // Parse robots
    let robots = parse(template, dims);

    // Iterate on robots
    let expected_size = robots.len();
    let mut i = 0;
    loop {
        i += 1;

        // Move all and keep positions in a set
        let mut plots: HashSet<(i32, i32)> = HashSet::new();
        for r in &robots {
            let (x, y) = r.mv(i);
            plots.insert((x, y));
        }
        if plots.len() == expected_size {
            break;
        }
    }
    println!("Solution 2 for {}: {}", template, i);
}

fn main() {
    step1("sample", (11, 7));
    step1("input", (101, 103));
    step2("input", (101, 103));
}
