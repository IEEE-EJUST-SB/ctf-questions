package main

import (
	"fmt"
	"math/big"
)

// Power calculates (base^expo) % m efficiently
func power(base, expo, m *big.Int) *big.Int {
	res := big.NewInt(1)
	base = new(big.Int).Mod(base, m)
	for expo.Cmp(big.NewInt(0)) > 0 {
		if new(big.Int).And(expo, big.NewInt(1)).Cmp(big.NewInt(0)) != 0 {
			res = new(big.Int).Mod(new(big.Int).Mul(res, base), m)
		}
		base = new(big.Int).Mod(new(big.Int).Mul(base, base), m)
		expo = new(big.Int).Div(expo, big.NewInt(2))
	}
	return res
}

// ExtendedGCD computes gcd(a, b) and coefficients x, y such that ax + by = gcd(a, b)
func extendedGCD(a, b *big.Int) (*big.Int, *big.Int, *big.Int) {
	x, y := big.NewInt(0), big.NewInt(1)
	lastX, lastY := big.NewInt(1), big.NewInt(0)
	for b.Cmp(big.NewInt(0)) != 0 {
		quotient := new(big.Int).Div(a, b)
		a, b = b, new(big.Int).Mod(a, b)
		lastX, x = x, new(big.Int).Sub(lastX, new(big.Int).Mul(quotient, x))
		lastY, y = y, new(big.Int).Sub(lastY, new(big.Int).Mul(quotient, y))
	}
	return a, lastX, lastY
}

// ModInverse finds the modular inverse of e modulo phi using Extended Euclidean Algorithm
func modInverse(e, phi *big.Int) *big.Int {
	gcd, x, _ := extendedGCD(e, phi)
	if gcd.Cmp(big.NewInt(1)) != 0 {
		return big.NewInt(-1) // No modular inverse exists
	}
	// Ensure x is positive
	if x.Cmp(big.NewInt(0)) < 0 {
		x = new(big.Int).Add(x, phi)
	}
	return new(big.Int).Mod(x, phi)
}

// GenerateKeys generates RSA public and private keys
func generateKeys() (*big.Int, *big.Int, *big.Int) {
	// Initialize large primes using SetString to avoid int64 overflow
	p, _ := new(big.Int).SetString("1617549722683965197900599011412144490161", 10)
	q, _ := new(big.Int).SetString("475693130177488446807040098678772442581573", 10)

	n := new(big.Int).Mul(p, q)
	phi := new(big.Int).Mul(new(big.Int).Sub(p, big.NewInt(1)), new(big.Int).Sub(q, big.NewInt(1)))

	// Set e = 65537
	e := big.NewInt(65537)
	if gcd(e, phi).Cmp(big.NewInt(1)) != 0 {
		panic("e=65537 is not coprime with phi(n)")
	}

	// Compute d such that e * d ≡ 1 (mod phi(n))
	d := modInverse(e, phi)
	if d.Cmp(big.NewInt(-1)) == 0 {
		panic("Failed to find modular inverse")
	}

	return e, d, n
}

// Gcd calculates the greatest common divisor
func gcd(a, b *big.Int) *big.Int {
	a = new(big.Int).Set(a)
	b = new(big.Int).Set(b)
	for b.Cmp(big.NewInt(0)) != 0 {
		a, b = b, new(big.Int).Mod(a, b)
	}
	return a
}

// Encrypt encrypts message using public key (e, n)
func encrypt(m, e, n *big.Int) *big.Int {
	return power(m, e, n)
}

// Decrypt decrypts message using private key (d, n)
func decrypt(c, d, n *big.Int) *big.Int {
	return power(c, d, n)
}

func main() {
	// Key Generation
	e, d, n := generateKeys()

	fmt.Printf("Public Key (e, n): (%s, %s)\n", e.String(), n.String())
	fmt.Printf("Private Key (d, n): (%s, %s)\n", d.String(), n.String())

	// Input string message
	message := "DEVSTORM{FLAG}"
	fmt.Printf("Original Message: %s\n", message)

	// Convert string to big.Int (using bytes)
	m := new(big.Int).SetBytes([]byte(message))

	// Encrypt the message
	c := encrypt(m, e, n)
	fmt.Printf("Encrypted Message (as number): %s\n", c.String())

	// Decrypt the message
	decryptedNum := decrypt(c, d, n)
	// Convert back to string
	decryptedBytes := decryptedNum.Bytes()
	decryptedMessage := string(decryptedBytes)
	fmt.Printf("Decrypted Message: %s\n", decryptedMessage)
}
