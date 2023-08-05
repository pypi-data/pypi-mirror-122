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
    // add a 2 to the start
    primes.splice(0..0, [2].iter().cloned());
    return primes;
}


#[pyfunction]
/// Checks whether a given number is prime
fn is_prime(number_being_checked: u64) -> bool {
    // Assumes that n is a positive natural number
    // We know 1 is not a prime number
    if number_being_checked == 1 {
        return false;
    }

    let mut i = 2;
            // This will loop from 2 to int(sqrt(x))
    while i * i <= number_being_checked {
            // Check if i divides x without leaving a remainder
        if number_being_checked % i == 0 {
            // This means that n has a factor in between 2 and sqrt(n)
            // So it is not a prime number
            return false;
        }
        i += 1;
    }
    // If we did not find any factor in the above loop,
    // then n is a prime number
    return true;
}

#[pymodule]
fn primetools(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_primes_to, m)?)?;
    m.add_function(wrap_pyfunction!(is_prime, m)?)?;
    Ok(())
}
