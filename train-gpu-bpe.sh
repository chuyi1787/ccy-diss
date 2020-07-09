export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

type=bpe
languages="English Arabic Turkish Spanish"

batch_size=60
burn_in_for_n_epochs=10
patience=10 # early_stopping_n_epochs
val_every_n_epochs=1


for lang in ${languages}
do
datadir=${lang}-${type}

echo "Sarting training"
echo ${datadir}
steps_of_an_epoch=($(wc -l ./data/${datadir}/train-sources))
#use the first 10 epochs as a burn-in period
validBurnIn=$((steps_of_an_epoch *${burn_in_for_n_epochs} / ${batch_size}))
# early stopping with patience 10
early_stopping_steps=$((steps_of_an_epoch *${patience} / ${batch_size}))
# validate every epoch
val_steps=$((steps_of_an_epoch *${val_every_n_epochs}/ ${batch_size}))


onmt_train -data models/${datadir}/data-pp/${datadir}\
  --save_model models/${datadir}/${lang}-${type}-\
  --encoder_type brnn\
  --decoder_type rnn\
  --enc_layers 2\
  --dec_layers 2\
  --rnn_type GRU\
  --batch_size 60\
  --src_word_vec_size 300\
  --tgt_word_vec_size 300\
  --rnn_size 100\
  --optim "adadelta" \
  --dropout 0.2\
  --early_stopping ${early_stopping_steps}\
  --valid_steps ${val_steps}\
  --warmup_steps ${validBurnIn}\
  --train_steps 3000000\
  --report_every 500 \
  --gpu_ranks 0 &> train-gpu.log &
echo "End of training"


#echo "Lemmatizing test set"
#onmt_translate \
#  --model demo-model_XYZ.pt\
#  --src data/src-test.txt\
#  --output pred.txt\
#  --replace_unk\
#  --beam_size 12\
#  --verbose
#echo "Done"



done












