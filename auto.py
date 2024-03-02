import time  # Import library time untuk menggunakan fungsi sleep

from web3 import Web3

# Inisialisasi sebuah instance Web3 dengan menggunakan provider EVMOS Testnet
w3 = Web3(Web3.HTTPProvider('https://evmos-testnet.lava.build/lava-referer-6a831606-2433-424f-b25c-1a68896f2dca/'))

# Alamat dompet pengirim
sender_address = 'addres'
private_key = 'privat anda'

# Buat objek Account dari kunci pribadi
sender_account = w3.eth.account.from_key(private_key)

# Alamat dompet penerima
receiver_address = 'penerima'

# Loop sampai saldo habis
while w3.eth.get_balance(sender_address) > 0:
    # Jumlah tEVMOS yang ingin dikirim
    total_amount = w3.to_wei(0.001, 'ether')  # Mengonversi ke satuan wei
    amount_to_send = total_amount

    # Perkirakan biaya gas
    gas_estimate = w3.eth.estimate_gas({'to': receiver_address, 'value': amount_to_send})

    # Batasi biaya gas sesuai dengan gas limit yang ditetapkan
    gas_limit = min(50000, gas_estimate)

    # Buat transaksi
    transaction = {
        'to': receiver_address,
        'value': min(amount_to_send, w3.eth.get_balance(sender_address)),  # Memperbaiki kesalahan nama metode
        'gas': gas_limit,  # Gunakan gas limit yang ditetapkan
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(sender_account.address),
        'chainId': 9000,  # Menyertakan chain ID untuk jaringan EVMOS Testnet
    }

    # Tandatangani transaksi
    signed_txn = sender_account.sign_transaction(transaction)  # Juga pastikan ini sesuai dengan konvensi penamaan yang benar

    # Kirim transaksi
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print("Transaksi berhasil dikirim. Hash transaksi:", tx_hash.hex())

    # Jeda waktu 10 detik sebelum pengiriman transaksi berikutnya
    time.sleep(10)
