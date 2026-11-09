SID:
        .word   1230016
notlar:
        .zero   160
bucket:
        .zero   20
mean:
        .zero   4
below_count:
        .zero   4
pass_count:
        .zero   4
grup:
        addi    sp,sp,-32
        sw      ra,28(sp)
        sw      s0,24(sp)
        addi    s0,sp,32
        sw      a0,-20(s0)
        lw      a4,-20(s0)
        li      a5,49
        bgt     a4,a5,.L2
        li      a5,0
        j       .L3
.L2:
        lw      a4,-20(s0)
        li      a5,64
        bgt     a4,a5,.L4
        li      a5,1
        j       .L3
.L4:
        lw      a4,-20(s0)
        li      a5,74
        bgt     a4,a5,.L5
        li      a5,2
        j       .L3
.L5:
        lw      a4,-20(s0)
        li      a5,84
        bgt     a4,a5,.L6
        li      a5,3
        j       .L3
.L6:
        li      a5,4
.L3:
        mv      a0,a5
        lw      ra,28(sp)
        lw      s0,24(sp)
        addi    sp,sp,32
        jr      ra
main:
        addi    sp,sp,-48
        sw      ra,44(sp)
        sw      s0,40(sp)
        addi    s0,sp,48
        li      a5,1228800
        addi    a5,a5,1216
        sw      a5,-20(s0)
        sw      zero,-24(s0)
        li      a5,1228800
        addi    a3,a5,1216
        li      a5,1717985280
        addi    a5,a5,1639
        mulh    a5,a3,a5
        srai    a4,a5,2
        srai    a5,a3,31
        sub     a4,a4,a5
        mv      a5,a4
        slli    a5,a5,2
        add     a5,a5,a4
        slli    a5,a5,1
        sub     a4,a3,a5
        addi    a5,a4,50
        sw      a5,-40(s0)
        sw      zero,-28(s0)
        j       .L8
.L9:
        lw      a4,-20(s0)
        li      a5,1662976
        addi    a5,a5,1549
        mul     a4,a4,a5
        li      a5,1013903360
        addi    a5,a5,863
        add     a5,a4,a5
        sw      a5,-20(s0)
        lw      a5,-20(s0)
        srli    a5,a5,16
        li      a4,1148157952
        addi    a4,a4,1623
        mulhu   a4,a5,a4
        sub     a3,a5,a4
        srli    a3,a3,1
        add     a4,a4,a3
        srli    a4,a4,6
        li      a3,101
        mul     a4,a4,a3
        sub     a4,a5,a4
        mv      a3,a4
        lla     a4,notlar
        lw      a5,-28(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        sw      a3,0(a5)
        lw      a5,-28(s0)
        addi    a5,a5,1
        sw      a5,-28(s0)
.L8:
        lw      a4,-28(s0)
        li      a5,39
        ble     a4,a5,.L9
        sw      zero,-32(s0)
        j       .L10
.L12:
        lla     a4,notlar
        lw      a5,-32(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a5,0(a5)
        lw      a4,-24(s0)
        add     a5,a4,a5
        sw      a5,-24(s0)
        lla     a4,notlar
        lw      a5,-32(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a5,0(a5)
        mv      a0,a5
        call    grup
        mv      a5,a0
        lla     a3,bucket
        slli    a4,a5,2
        add     a4,a3,a4
        lw      a4,0(a4)
        addi    a4,a4,1
        lla     a3,bucket
        slli    a5,a5,2
        add     a5,a3,a5
        sw      a4,0(a5)
        lla     a4,notlar
        lw      a5,-32(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a5,0(a5)
        lw      a4,-40(s0)
        bgt     a4,a5,.L11
        lla     a5,pass_count
        lw      a5,0(a5)
        addi    a4,a5,1
        lla     a5,pass_count
        sw      a4,0(a5)
.L11:
        lw      a5,-32(s0)
        addi    a5,a5,1
        sw      a5,-32(s0)
.L10:
        lw      a4,-32(s0)
        li      a5,39
        ble     a4,a5,.L12
        lw      a5,-24(s0)
        li      a4,1717985280
        addi    a4,a4,1639
        mulh    a4,a5,a4
        srai    a4,a4,4
        srai    a5,a5,31
        sub     a4,a4,a5
        lla     a5,mean
        sw      a4,0(a5)
        sw      zero,-36(s0)
        j       .L13
.L15:
        lla     a4,notlar
        lw      a5,-36(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a4,0(a5)
        lla     a5,mean
        lw      a5,0(a5)
        bge     a4,a5,.L14
        lla     a4,notlar
        lw      a5,-36(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a5,0(a5)
        ori     a4,a5,256
        lla     a3,notlar
        lw      a5,-36(s0)
        slli    a5,a5,2
        add     a5,a3,a5
        sw      a4,0(a5)
        lla     a5,below_count
        lw      a5,0(a5)
        addi    a4,a5,1
        lla     a5,below_count
        sw      a4,0(a5)
.L14:
        lw      a5,-36(s0)
        addi    a5,a5,1
        sw      a5,-36(s0)
.L13:
        lw      a4,-36(s0)
        li      a5,39
        ble     a4,a5,.L15
        li      a5,0
        mv      a0,a5
        lw      ra,44(sp)
        lw      s0,40(sp)
        addi    sp,sp,48
        jr      ra
