while IFS= read -r pid; do
    kill "$pid"
done < pids.log
