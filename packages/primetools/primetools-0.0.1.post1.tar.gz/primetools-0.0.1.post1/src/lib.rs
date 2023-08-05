use pyo3::prelude::*;

#[pyfunction]
/// Gets all the prime numbers up to the specified value
fn get_primes_to(largest_number_wanted: u128) -> Vec<u128> {
    let mut primes: Vec<u128> = Vec::new();
    let m: usize = ((largest_number_wanted - 2) / 2) as usize;
    let mut candidates: Vec<bool> = vec![true; m];
    for j in 1..m {
        for i in 1..j + 1 {
            let not_prime = i + j + 2 * i * j;
            if not_prime > m {
                break;
            }
            candidates[not_prime - 1] = false;
        }
    }

    // Put primes in list
    for (i, c) in candidates.iter().enumerate() {
        if *c {
            let prime = 1 + 2 * (i + 1) as u128;
            primes.push(prime);
        }
    }
    return primes;
}

#[pyfunction]
/// Gets a certain amount of prime numbers
fn get_primes_amount(count: u128) -> Vec<u128> {
    let mut primes = vec![true; (count + 1) as usize];
    let mut p = 2;
    while p * p <= count {
        if primes[p as usize] {
            let mut index = p * p;
            while index <= count {
                primes[index as usize] = false;
                index += p;
            }
        }

        p += 1;
    }
    let mut result = vec![];
    for (i, p) in primes.iter().enumerate() {
        if *p {
            result.push(i as u128);
        }
    }
    result.remove(0);
    result.remove(0);
    return result;
}

#[pymodule]
fn primetools(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_primes_to, m)?)?;
    m.add_function(wrap_pyfunction!(get_primes_amount, m)?)?;
    Ok(())
}
