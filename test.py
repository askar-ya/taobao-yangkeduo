text = 'askar and evi love appel and juise'
chunk_size = 5
chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
for chunk in chunks:
    print(chunk)
