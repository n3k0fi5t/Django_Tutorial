<template>
    <Card :padding="padding" :shadow="shadow" :bordered="bordered">
        <div slot="title" class="panel-title">
        <slot name="title"></slot>
        </div>
        <div slot="extra" class="panel-extra">
        <slot name="extra"></slot>
        </div>
        <div class="panel-body">
        <slot></slot>
        </div>
    </Card>
</template>

<script>
    export default {
        name: 'Panel',
        props: {
            shadow: {
                required: false,
                type: Boolean,
                default: false,
            },
            padding: {
                required: false,
                type: Number,
                default: 0,
            },
            bordered: {
                required: false,
                type: Boolean,
                default: true,
            },
        }
    }
</script>

<style lang="less">
  .panel-title {
    font-size: 21px;
    font-weight: 500;
    padding-top: 10px;
    padding-bottom: 20px;
    line-height: 30px;
    padding: 5px 15px;
  }
  .panel-extra {
    line-height: 40px;
    .ivu-input-icon {
      line-height: 40px;
    }
  }
  .panel-body {
    word-break: break-all;
    word-wrap: break-word;
    width: 100%;
  }

</style>