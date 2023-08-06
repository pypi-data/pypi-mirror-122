# tkitAutoMask

自动构建掩码

```
pip install tkitAutoMask


```



```python
from tkitAutoMask import autoMask
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained("uer/chinese_roberta_L-2_H-128") 
# dir(tokenizer)
tomask = autoMask(
    # transformer,
    mask_token_id = tokenizer.mask_token_id,          # the token id reserved for masking
    pad_token_id = tokenizer.pad_token_id,           # the token id for padding
    mask_prob = 0.05,           # masking probability for masked language modeling
    replace_prob = 0.90,        # ~10% probability that token will not be masked, but included in loss, as detailed in the epaper
    mask_ignore_token_ids = [tokenizer.cls_token_id,tokenizer.eos_token_id]  # other tokens to exclude from masking, include the [cls] and [sep] here
)
 
```

详细参考

> dev.md


