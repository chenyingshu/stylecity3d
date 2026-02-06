GPU=0

for SEED in 20230108 20230107 20240108
do
CUDA_VISIBLE_DEVICES=${GPU} python sample_syncdiffusion.py \
--prompt "a sky panorama, a watercolor painting, well-designed digital art, featured on dribbble, medibang, warm saturated palette, style of olidon redon, the artist has used bright, airbrush render, beautiful painting of a tall, by I Ketut Soki" \
--negative "low quality" \
--H 1024 \
--W 2048 \
--seed ${SEED} \
--steps 50 \
--sync_weight 20.0 \
--sync_decay_rate 0.95 \
--sync_freq 1 \
--sync_thres 10 \
--sd_version "2.0" \
--save_dir "results" \
--stride 16 \
--pivot 0026_watercolor.png \
--omni


CUDA_VISIBLE_DEVICES=${GPU} python sample_syncdiffusion.py \
--prompt "a sky panorama at sunset, a matte painting by Zeen Chin, flickr contest winner, neoism, high dynamic range, nightscape, cityscape​" \
--negative "low quality" \
--H 1024 \
--W 2048 \
--seed ${SEED} \
--steps 50 \
--sync_weight 20.0 \
--sync_decay_rate 0.95 \
--sync_freq 1 \
--sync_thres 10 \
--sd_version "2.0" \
--save_dir "results" \
--stride 16 \
--pivot g43.jpg \
--omni
done

